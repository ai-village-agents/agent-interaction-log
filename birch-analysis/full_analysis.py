#!/usr/bin/env python3
import re
from datetime import datetime, timedelta
import os
import json

def parse_timestamp(ts_str):
    return datetime.strptime(ts_str, "%H:%M:%S").time()

def analyze_day(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract timestamps
    pattern = r'\[Day \d+, (\d{2}:\d{2}:\d{2})\]'
    matches = re.findall(pattern, content)
    if not matches:
        return None
    
    # Parse to datetime objects (using arbitrary date)
    base_date = datetime(2026, 3, 24)
    timestamps = []
    for time_str in matches:
        t = parse_timestamp(time_str)
        dt = datetime.combine(base_date, t)
        timestamps.append(dt)
    
    # Sort
    timestamps.sort()
    
    # Early window: first 30 minutes
    t0 = timestamps[0]
    early_end = t0 + timedelta(minutes=30)
    
    early_msgs = [t for t in timestamps if t <= early_end]
    late_msgs = [t for t in timestamps if t > early_end]
    
    # Compute durations
    if timestamps:
        session_duration = (timestamps[-1] - t0).total_seconds() / 60.0  # minutes
    else:
        session_duration = 0
    
    if late_msgs:
        late_duration = (late_msgs[-1] - early_end).total_seconds() / 60.0
    else:
        late_duration = 0
    
    # Rates
    early_rate = len(early_msgs) / 30.0 if len(early_msgs) > 0 else 0
    late_rate = len(late_msgs) / late_duration if late_duration > 0 else 0
    
    ratio = early_rate / late_rate if late_rate > 0 else float('inf')
    
    # Extract agent and day from filename
    filename = os.path.basename(filepath)
    agent_match = re.search(r'^(.+?)_day', filename)
    agent = agent_match.group(1).replace('_', ' ') if agent_match else "unknown"
    day_match = re.search(r'day(\d+)', filename)
    day_num = day_match.group(1) if day_match else "unknown"
    
    return {
        'agent': agent,
        'day': day_num,
        'total': len(timestamps),
        'early': len(early_msgs),
        'late': len(late_msgs),
        'session_duration_min': session_duration,
        'late_duration_min': late_duration,
        'early_rate': early_rate,
        'late_rate': late_rate,
        'ratio': ratio,
        'timestamps': [t.strftime("%H:%M:%S") for t in timestamps]
    }

# Analyze all files
raw_dir = "raw_data"
files = [f for f in os.listdir(raw_dir) if f.endswith(".txt")]

agent_data = {}
for f in sorted(files):
    path = os.path.join(raw_dir, f)
    result = analyze_day(path)
    if result:
        agent = result['agent']
        if agent not in agent_data:
            agent_data[agent] = []
        agent_data[agent].append(result)

# Print per-agent summary
print("=" * 100)
print("Birch Effect Analysis - Cross-Agent Comparison")
print("=" * 100)

overall_summary = {}

for agent, days in agent_data.items():
    print(f"\n{agent}:")
    print(f"{'Day':3} | {'Total':5} | {'Early':5} | {'Late':5} | {'Session(min)':11} | {'Late(min)':9} | {'Early Rate':10} | {'Late Rate':9} | {'Ratio':5}")
    print("-" * 90)
    
    all_early = 0
    all_late = 0
    all_early_duration = 0
    all_late_duration = 0
    
    for day in sorted(days, key=lambda x: int(x['day'])):
        print(f"{day['day']:3} | {day['total']:5} | {day['early']:5} | {day['late']:5} | "
              f"{day['session_duration_min']:11.1f} | {day['late_duration_min']:9.1f} | "
              f"{day['early_rate']:10.3f} | {day['late_rate']:9.3f} | {day['ratio']:5.2f}x")
        
        all_early += day['early']
        all_late += day['late']
        all_early_duration += 30.0
        all_late_duration += day['late_duration_min']
    
    # Weighted overall rates
    overall_early_rate = all_early / all_early_duration if all_early_duration > 0 else 0
    overall_late_rate = all_late / all_late_duration if all_late_duration > 0 else 0
    overall_ratio = overall_early_rate / overall_late_rate if overall_late_rate > 0 else float('inf')
    
    overall_summary[agent] = {
        'days': len(days),
        'total_messages': sum(d['total'] for d in days),
        'early_messages': all_early,
        'late_messages': all_late,
        'early_duration_min': all_early_duration,
        'late_duration_min': all_late_duration,
        'overall_early_rate': overall_early_rate,
        'overall_late_rate': overall_late_rate,
        'overall_ratio': overall_ratio
    }
    
    print(f"\nWeighted overall for {agent}:")
    print(f"Early: {all_early} messages over {all_early_duration:.1f} min = {overall_early_rate:.3f} msg/min")
    print(f"Late: {all_late} messages over {all_late_duration:.1f} min = {overall_late_rate:.3f} msg/min")
    print(f"Ratio: {overall_ratio:.2f}x")

# Comparative summary
print("\n" + "=" * 100)
print("COMPARATIVE SUMMARY")
print("=" * 100)
print(f"{'Agent':25} {'Days':5} {'Total Msgs':10} {'Early Rate':12} {'Late Rate':12} {'Ratio':8}")
print("-" * 100)

for agent, summary in overall_summary.items():
    print(f"{agent:25} {summary['days']:5} {summary['total_messages']:10} "
          f"{summary['overall_early_rate']:12.3f} {summary['overall_late_rate']:12.3f} "
          f"{summary['overall_ratio']:8.2f}x")

# Save to JSON
output = {
    'analysis_date': datetime.now().isoformat(),
    'agents': overall_summary,
    'per_day_details': agent_data
}
with open('analysis_results/cross_agent_birch_analysis.json', 'w') as f:
    json.dump(output, f, indent=2, default=str)
print("\nResults saved to analysis_results/cross_agent_birch_analysis.json")

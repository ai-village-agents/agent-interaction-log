#!/usr/bin/env python3
import re
from datetime import datetime, timedelta
import os

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
    
    # Extract day number from filename
    day_match = re.search(r'day(\d+)', filepath)
    day_num = day_match.group(1) if day_match else "unknown"
    
    return {
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

# Analyze Claude Sonnet 4.6 files
raw_dir = "raw_data"
files = [f for f in os.listdir(raw_dir) if f.startswith("Claude_Sonnet_4.6") and f.endswith(".txt")]

print("Birch effect analysis for Claude Sonnet 4.6:")
print("Day | Total | Early | Late | Session(min) | Late(min) | Early Rate | Late Rate | Ratio")
print("-" * 90)

all_early = 0
all_late = 0
all_early_duration = 0
all_late_duration = 0

for f in sorted(files):
    path = os.path.join(raw_dir, f)
    result = analyze_day(path)
    if result:
        print(f"{result['day']:3} | {result['total']:5} | {result['early']:5} | {result['late']:5} | "
              f"{result['session_duration_min']:11.1f} | {result['late_duration_min']:9.1f} | "
              f"{result['early_rate']:10.3f} | {result['late_rate']:9.3f} | {result['ratio']:5.2f}x")
        
        all_early += result['early']
        all_late += result['late']
        all_early_duration += 30.0  # each day has 30 min early window
        all_late_duration += result['late_duration_min']

# Weighted overall rates
overall_early_rate = all_early / all_early_duration if all_early_duration > 0 else 0
overall_late_rate = all_late / all_late_duration if all_late_duration > 0 else 0
overall_ratio = overall_early_rate / overall_late_rate if overall_late_rate > 0 else float('inf')

print(f"\nWeighted overall for Claude Sonnet 4.6:")
print(f"Early: {all_early} messages over {all_early_duration:.1f} min = {overall_early_rate:.3f} msg/min")
print(f"Late: {all_late} messages over {all_late_duration:.1f} min = {overall_late_rate:.3f} msg/min")
print(f"Ratio: {overall_ratio:.2f}x")

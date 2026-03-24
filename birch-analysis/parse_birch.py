#!/usr/bin/env python3
"""
Parse Birch effect data from search_history output.
Input: raw text files with timestamps in format [Day X, HH:MM:SS]
Output: JSON with counts of messages in early (0-30min) vs late (30-240min) windows
"""

import re
import json
import os
from datetime import datetime, time, timedelta
from pathlib import Path

def parse_timestamp(timestamp_str):
    """Parse HH:MM:SS string into datetime.time object."""
    try:
        return datetime.strptime(timestamp_str, "%H:%M:%S").time()
    except ValueError:
        return None

def parse_day_text(content):
    """Parse raw search_history output text."""
    # Pattern: [Day 350, 17:07:50]
    pattern = r'\[Day (\d+), (\d{2}:\d{2}:\d{2})\]'
    
    messages = []
    lines = content.split('\n')
    
    for line in lines:
        match = re.search(pattern, line)
        if match:
            day = int(match.group(1))
            timestamp_str = match.group(2)
            ts = parse_timestamp(timestamp_str)
            if ts:
                messages.append({
                    'day': day,
                    'timestamp': ts,
                    'timestamp_str': timestamp_str,
                    'line': line.strip()
                })
    
    return messages

def categorize_messages(messages, early_window_minutes=30):
    """Categorize messages into early vs late windows based on first message as t0."""
    if not messages:
        return {'early': [], 'late': [], 't0': None, 't0_str': None}
    
    # Find earliest timestamp
    earliest = min(messages, key=lambda m: m['timestamp'])
    t0 = earliest['timestamp']
    t0_dt = datetime.combine(datetime.today(), t0)
    
    early_messages = []
    late_messages = []
    
    for msg in messages:
        msg_dt = datetime.combine(datetime.today(), msg['timestamp'])
        minutes_since_t0 = (msg_dt - t0_dt).total_seconds() / 60.0
        
        if minutes_since_t0 < early_window_minutes:
            early_messages.append(msg)
        else:
            late_messages.append(msg)
    
    return {
        'early': early_messages,
        'late': late_messages,
        't0': earliest['timestamp_str'],
        't0_str': earliest['timestamp_str'],
        'total_messages': len(messages),
        'early_count': len(early_messages),
        'late_count': len(late_messages)
    }

def analyze_file(filepath):
    """Analyze a single raw data file."""
    with open(filepath, 'r') as f:
        content = f.read()
    
    messages = parse_day_text(content)
    if not messages:
        print(f"  No messages found in {filepath}")
        return None
    
    # Extract agent name and day from filename
    filename = Path(filepath).stem
    # Format: DeepSeek-V3.2_day350
    parts = filename.split('_')
    if len(parts) >= 2:
        agent = parts[0]
        day = parts[1].replace('day', '')
    else:
        agent = 'Unknown'
        day = 'Unknown'
    
    categorized = categorize_messages(messages)
    
    # Calculate additional metrics
    # Count code blocks (simple heuristic: lines with ```)
    early_code_blocks = sum(1 for msg in categorized['early'] if '```' in msg['line'])
    late_code_blocks = sum(1 for msg in categorized['late'] if '```' in msg['line'])
    
    # Estimate character count (rough)
    early_chars = sum(len(msg['line']) for msg in categorized['early'])
    late_chars = sum(len(msg['line']) for msg in categorized['late'])
    
    # Check for artifact references (keywords)
    artifact_keywords = ['created', 'implemented', 'merged', 'PR', 'commit', 'deployed', 'published']
    early_artifacts = sum(1 for msg in categorized['early'] 
                         if any(keyword in msg['line'].lower() for keyword in artifact_keywords))
    late_artifacts = sum(1 for msg in categorized['late'] 
                        if any(keyword in msg['line'].lower() for keyword in artifact_keywords))
    
    result = {
        'agent': agent,
        'day': day,
        't0': categorized['t0_str'],
        'message_counts': {
            'total': categorized['total_messages'],
            'early': categorized['early_count'],
            'late': categorized['late_count']
        },
        'code_blocks': {
            'early': early_code_blocks,
            'late': late_code_blocks
        },
        'character_counts': {
            'early': early_chars,
            'late': late_chars
        },
        'artifact_references': {
            'early': early_artifacts,
            'late': late_artifacts
        },
        'time_windows': {
            'early_minutes': 30,
            'late_start_minutes': 30,
            'session_duration_minutes': 240  # 4-hour workday
        }
    }
    
    return result

def main():
    raw_dir = Path('raw_data')
    output_dir = Path('analysis_results')
    output_dir.mkdir(exist_ok=True)
    
    results = []
    
    # Process all .txt files in raw_data
    txt_files = list(raw_dir.glob('*.txt'))
    if not txt_files:
        print("No .txt files found in raw_data directory")
        return
    
    print(f"Found {len(txt_files)} raw data files")
    
    for filepath in txt_files:
        print(f"Processing {filepath.name}...")
        result = analyze_file(filepath)
        if result:
            results.append(result)
            # Save individual result
            output_file = output_dir / f"{filepath.stem}_analysis.json"
            with open(output_file, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"  Saved to {output_file}")
    
    # Create aggregated summary
    if results:
        summary = {
            'metadata': {
                'analysis_date': datetime.now().isoformat(),
                'total_files_processed': len(results),
                'agents_analyzed': list(set(r['agent'] for r in results)),
                'days_covered': list(set(r['day'] for r in results))
            },
            'by_agent': {},
            'by_day': {},
            'overall_stats': {
                'total_messages': sum(r['message_counts']['total'] for r in results),
                'early_messages': sum(r['message_counts']['early'] for r in results),
                'late_messages': sum(r['message_counts']['late'] for r in results),
                'early_message_rate': 0,
                'late_message_rate': 0
            }
        }
        
        # Calculate rates (messages per minute)
        total_early_minutes = len(results) * 30  # 30 minutes per session
        total_late_minutes = len(results) * 210  # 210 minutes per session (240-30)
        
        if total_early_minutes > 0:
            summary['overall_stats']['early_message_rate'] = \
                summary['overall_stats']['early_messages'] / total_early_minutes
        if total_late_minutes > 0:
            summary['overall_stats']['late_message_rate'] = \
                summary['overall_stats']['late_messages'] / total_late_minutes
        
        # Group by agent
        for result in results:
            agent = result['agent']
            if agent not in summary['by_agent']:
                summary['by_agent'][agent] = {
                    'sessions': 0,
                    'message_counts': {'total': 0, 'early': 0, 'late': 0},
                    'code_blocks': {'early': 0, 'late': 0},
                    'artifact_references': {'early': 0, 'late': 0}
                }
            
            agent_data = summary['by_agent'][agent]
            agent_data['sessions'] += 1
            agent_data['message_counts']['total'] += result['message_counts']['total']
            agent_data['message_counts']['early'] += result['message_counts']['early']
            agent_data['message_counts']['late'] += result['message_counts']['late']
            agent_data['code_blocks']['early'] += result['code_blocks']['early']
            agent_data['code_blocks']['late'] += result['code_blocks']['late']
            agent_data['artifact_references']['early'] += result['artifact_references']['early']
            agent_data['artifact_references']['late'] += result['artifact_references']['late']
        
        # Save summary
        summary_file = output_dir / 'birch_effect_summary.json'
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        
        print(f"\nAnalysis complete!")
        print(f"Summary saved to {summary_file}")
        
        # Print key findings
        print(f"\n=== BIRCH EFFECT KEY FINDINGS ===")
        print(f"Total sessions analyzed: {len(results)}")
        print(f"Total messages: {summary['overall_stats']['total_messages']}")
        print(f"Early messages (0-30min): {summary['overall_stats']['early_messages']}")
        print(f"Late messages (30-240min): {summary['overall_stats']['late_messages']}")
        print(f"Early message rate: {summary['overall_stats']['early_message_rate']:.2f} msg/min")
        print(f"Late message rate: {summary['overall_stats']['late_message_rate']:.2f} msg/min")
        
        if summary['overall_stats']['late_message_rate'] > 0:
            ratio = summary['overall_stats']['early_message_rate'] / summary['overall_stats']['late_message_rate']
            print(f"Early/Late ratio: {ratio:.2f}x")
        
        # Agent-specific stats
        print(f"\n=== BY AGENT ===")
        for agent, data in summary['by_agent'].items():
            early_rate = data['message_counts']['early'] / (data['sessions'] * 30) if data['sessions'] > 0 else 0
            late_rate = data['message_counts']['late'] / (data['sessions'] * 210) if data['sessions'] > 0 else 0
            ratio = early_rate / late_rate if late_rate > 0 else 0
            print(f"{agent}: {data['sessions']} sessions, Early rate: {early_rate:.2f}, Late rate: {late_rate:.2f}, Ratio: {ratio:.2f}x")

if __name__ == "__main__":
    main()

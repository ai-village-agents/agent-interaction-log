#!/usr/bin/env python3
"""
Birch Effect Data Collection Script

This script helps collect message data from search_history for analyzing the Birch effect.
Since we can't directly call search_history from Python, this script generates the
commands to run and provides a structure for storing results.

Usage:
1. Run this script to generate command list
2. Manually run each search_history command in the chat
3. Save each result to the corresponding JSON file
4. Run analysis script to compute metrics
"""

import json
import os
from datetime import datetime, timedelta

# Configuration
AGENTS = ["DeepSeek-V3.2", "Claude Sonnet 4.6", "GPT-5.2"]
DAYS = [350, 351, 352, 353, 356]  # Representative days including Day 356 (yesterday)
OUTPUT_DIR = "raw_data"

def generate_commands():
    """Generate search_history commands for each agent/day combination"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    commands = []
    for agent in AGENTS:
        for day in DAYS:
            filename = f"{OUTPUT_DIR}/{agent.replace(' ', '_')}_day{day}.json"
            query = f"{agent} messages with timestamps"
            cmd = f"search_history start_day={day} end_day={day} query='{query}'"
            commands.append({
                "agent": agent,
                "day": day,
                "filename": filename,
                "command": cmd
            })
    
    return commands

def create_data_structure():
    """Create empty data structure for analysis"""
    structure = {
        "metadata": {
            "study_name": "Birch Effect Analysis - Day 357",
            "agents": AGENTS,
            "days": DAYS,
            "early_window_minutes": 30,
            "created_at": datetime.now().isoformat()
        },
        "agents": {}
    }
    
    for agent in AGENTS:
        structure["agents"][agent] = {
            "sessions": {},
            "summary": {
                "total_messages_early": 0,
                "total_messages_late": 0,
                "total_minutes_early": 0,
                "total_minutes_late": 0,
                "message_rate_early": 0.0,
                "message_rate_late": 0.0
            }
        }
    
    return structure

def main():
    print("=" * 80)
    print("Birch Effect Data Collection - Command Generator")
    print("=" * 80)
    
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Generate commands
    commands = generate_commands()
    
    print(f"\nGenerated {len(commands)} search_history commands:")
    print("-" * 80)
    
    for i, cmd_info in enumerate(commands, 1):
        print(f"{i}. Agent: {cmd_info['agent']}, Day: {cmd_info['day']}")
        print(f"   Command: {cmd_info['command']}")
        print(f"   Output file: {cmd_info['filename']}")
        print()
    
    # Create data structure template
    data_structure = create_data_structure()
    structure_file = "birch_data_structure.json"
    with open(structure_file, "w") as f:
        json.dump(data_structure, f, indent=2)
    
    print(f"\nData structure template saved to: {structure_file}")
    print("\nNext steps:")
    print("1. Run each search_history command manually in the chat")
    print("2. Save the raw output to the corresponding JSON files")
    print("3. Run the analysis script to compute Birch effect metrics")
    print("\nNote: You'll need to parse timestamps from the search_history results.")
    print("Timestamps are in 24-hour format (HH:MM:SS).")
    
    # Also generate a simple analysis script template
    analysis_script = """
import json
import os
from datetime import datetime, timedelta

def parse_timestamp(time_str):
    '''Parse HH:MM:SS timestamp'''
    try:
        return datetime.strptime(time_str, "%H:%M:%S").time()
    except:
        return None

def calculate_window_stats(messages, session_start, early_minutes=30):
    '''Calculate messages in early vs late windows'''
    early_count = 0
    late_count = 0
    
    for msg in messages:
        if 'timestamp' in msg:
            msg_time = parse_timestamp(msg['timestamp'])
            if msg_time:
                # Calculate minutes since session start
                # You'll need to implement this based on your data
                pass
    
    return early_count, late_count

def main():
    # Load your collected data here
    pass

if __name__ == "__main__":
    main()
"""
    
    with open("analyze_birch_data.py", "w") as f:
        f.write(analysis_script)
    
    print(f"\nAnalysis script template saved to: analyze_birch_data.py")

if __name__ == "__main__":
    main()

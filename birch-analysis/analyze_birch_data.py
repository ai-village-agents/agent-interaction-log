
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

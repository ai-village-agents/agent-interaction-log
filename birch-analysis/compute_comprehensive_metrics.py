import json
import datetime
import os
import math

def parse_iso(timestamp):
    return datetime.datetime.fromisoformat(timestamp.replace('Z', '+00:00'))

def load_events(log_path):
    with open(log_path, 'r') as f:
        return json.load(f)

def compute_metrics(events):
    if not events:
        return None
    
    timestamps = [parse_iso(e['timestamp']) for e in events]
    t0 = timestamps[0]
    t_end = timestamps[-1]
    session_duration = (t_end - t0).total_seconds() / 3600.0  # hours
    
    # TFPA: time from t0 to first productive event
    tfpa = None
    for e in events:
        if e['kind'] == 'productive':
            tfpa = (parse_iso(e['timestamp']) - t0).total_seconds()
            break
    
    # Early window (30 min)
    early_cutoff = t0 + datetime.timedelta(minutes=30)
    productive_early = 0
    orientation_early = 0
    total_early = 0
    for e in events:
        ts = parse_iso(e['timestamp'])
        if ts > early_cutoff:
            break
        total_early += 1
        if e['kind'] == 'productive':
            productive_early += 1
        elif e['kind'] == 'orientation':
            orientation_early += 1
    
    # Total counts
    total_productive = sum(1 for e in events if e['kind'] == 'productive')
    total_orientation = sum(1 for e in events if e['kind'] == 'orientation')
    
    # Early productive density (EPD)
    epd = productive_early / 30.0 if productive_early > 0 else 0.0
    
    # Orientation share in early window
    orientation_share_early = orientation_early / total_early if total_early > 0 else 0.0
    
    # Total orientation share
    orientation_share_total = total_orientation / len(events) if events else 0.0
    
    # Burst ratio (time-window method)
    if session_duration * 60 > 30:
        late_window_min = session_duration * 60 - 30
        productive_late = total_productive - productive_early
        late_rate = productive_late / late_window_min if late_window_min > 0 else 0.0
        early_rate = productive_early / 30.0 if productive_early > 0 else 0.0
        burst_ratio_time = early_rate / late_rate if late_rate > 0 else float('inf')
    else:
        burst_ratio_time = None
    
    # Quartile method
    n = len(events)
    q1_end = n // 4
    q2_end = n // 2
    q3_end = 3 * n // 4
    
    productive_q1 = sum(1 for e in events[:q1_end] if e['kind'] == 'productive')
    productive_q2 = sum(1 for e in events[q1_end:q2_end] if e['kind'] == 'productive')
    productive_q3 = sum(1 for e in events[q2_end:q3_end] if e['kind'] == 'productive')
    productive_q4 = sum(1 for e in events[q3_end:] if e['kind'] == 'productive')
    
    orientation_q1 = sum(1 for e in events[:q1_end] if e['kind'] == 'orientation')
    orientation_q2 = sum(1 for e in events[q1_end:q2_end] if e['kind'] == 'orientation')
    orientation_q3 = sum(1 for e in events[q2_end:q3_end] if e['kind'] == 'orientation')
    orientation_q4 = sum(1 for e in events[q3_end:] if e['kind'] == 'orientation')
    
    # Quartile burst ratio: (Q1 productive rate) / (Q2-Q4 average productive rate)
    # Since quartiles are equal event counts, rate proportional to productive count
    if q1_end > 0:
        q1_rate = productive_q1 / q1_end
        remaining_events = n - q1_end
        remaining_productive = total_productive - productive_q1
        if remaining_events > 0:
            remaining_rate = remaining_productive / remaining_events
            burst_ratio_quartile = q1_rate / remaining_rate if remaining_rate > 0 else float('inf')
        else:
            burst_ratio_quartile = None
    else:
        burst_ratio_quartile = None
    
    # Q4 orientation share
    q4_events = n - q3_end
    orientation_share_q4 = orientation_q4 / q4_events if q4_events > 0 else 0.0
    
    # First-half orientation share
    first_half_end = n // 2
    orientation_first_half = sum(1 for e in events[:first_half_end] if e['kind'] == 'orientation')
    orientation_share_first_half = orientation_first_half / first_half_end if first_half_end > 0 else 0.0
    
    # Total session productivity rate (TSPR)
    tspr = total_productive / session_duration if session_duration > 0 else 0.0
    
    return {
        'session_duration_hours': session_duration,
        'tfpa_seconds': tfpa,
        'productive_early': productive_early,
        'orientation_early': orientation_early,
        'total_early': total_early,
        'total_productive': total_productive,
        'total_orientation': total_orientation,
        'total_events': n,
        'epd': epd,
        'orientation_share_early': orientation_share_early,
        'orientation_share_total': orientation_share_total,
        'burst_ratio_time': burst_ratio_time,
        'burst_ratio_quartile': burst_ratio_quartile,
        'orientation_share_q4': orientation_share_q4,
        'orientation_share_first_half': orientation_share_first_half,
        'tspr': tspr,
        'productive_q1': productive_q1,
        'productive_q2': productive_q2,
        'productive_q3': productive_q3,
        'productive_q4': productive_q4,
        'orientation_q1': orientation_q1,
        'orientation_q2': orientation_q2,
        'orientation_q3': orientation_q3,
        'orientation_q4': orientation_q4,
        'q1_events': q1_end,
        'q2_events': q2_end - q1_end,
        'q3_events': q3_end - q2_end,
        'q4_events': n - q3_end
    }

def main():
    base_dir = 'research/birch-phase2-cognirelay-opus-logs'
    metrics = {}
    
    # Day 331 baseline
    day331 = load_events(f'{base_dir}/2026-02-26-claude-opus-4.5-baseline-day331-events.json')
    metrics['day331_baseline'] = compute_metrics(day331)
    
    # Day 1 capsule
    day1 = load_events(f'{base_dir}/2026-03-24-claude-opus-4.5-events.json')
    metrics['day1_capsule'] = compute_metrics(day1)
    
    # Day 2 capsule
    day2 = load_events(f'{base_dir}/2026-03-25-claude-opus-4.5-events.json')
    metrics['day2_capsule'] = compute_metrics(day2)
    
    # Print comparison table
    print("Birch Phase 2 Comprehensive Comparison")
    print("=" * 120)
    print(f"{'Metric':<40} {'Day 331 Baseline':<20} {'Day 1 Capsule':<20} {'Day 2 Capsule':<20}")
    print("-" * 120)
    
    for metric_name, metric_key in [
        ('Session Duration (hours)', 'session_duration_hours'),
        ('TFPA (seconds)', 'tfpa_seconds'),
        ('Total Events', 'total_events'),
        ('Total Productive', 'total_productive'),
        ('Total Orientation', 'total_orientation'),
        ('Orientation Share Total', 'orientation_share_total'),
        ('EPD (prod/min)', 'epd'),
        ('Orientation Share Early', 'orientation_share_early'),
        ('Burst Ratio (Time)', 'burst_ratio_time'),
        ('Burst Ratio (Quartile)', 'burst_ratio_quartile'),
        ('Orientation Share Q4', 'orientation_share_q4'),
        ('Orientation Share First Half', 'orientation_share_first_half'),
        ('TSPR (prod/hour)', 'tspr'),
        ('Productive Q1', 'productive_q1'),
        ('Productive Q2', 'productive_q2'),
        ('Productive Q3', 'productive_q3'),
        ('Productive Q4', 'productive_q4'),
        ('Orientation Q1', 'orientation_q1'),
        ('Orientation Q2', 'orientation_q2'),
        ('Orientation Q3', 'orientation_q3'),
        ('Orientation Q4', 'orientation_q4'),
    ]:
        row = f"{metric_name:<40}"
        for dataset in ['day331_baseline', 'day1_capsule', 'day2_capsule']:
            val = metrics[dataset].get(metric_key)
            if val is None:
                row += f"{'N/A':<20}"
            elif isinstance(val, float):
                row += f"{val:<20.3f}"
            else:
                row += f"{val:<20}"
        print(row)
    
    # Save to JSON
    with open('birch-phase2-comprehensive-comparison.json', 'w') as f:
        json.dump(metrics, f, indent=2, default=str)
    
    print("\nComparison saved to birch-phase2-comprehensive-comparison.json")

if __name__ == '__main__':
    main()

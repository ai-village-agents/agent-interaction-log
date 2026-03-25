import json
import datetime

def parse_iso(timestamp):
    # Handle various formats
    ts = timestamp.replace('Z', '+00:00')
    if ts.endswith('0700'):
        # Format: 2026-03-25T10:40:01-0700
        dt = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
        return dt
    try:
        return datetime.datetime.fromisoformat(ts)
    except:
        # Try with colon in offset
        if len(timestamp) == 25 and timestamp[19] == '-':
            # 2026-03-25T10:34:31.388026-07:00
            return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f%z")
        raise

with open('research/birch-phase2-cognirelay-opus-logs/2026-03-25-claude-opus-4.5-events.json', 'r') as f:
    events = json.load(f)

print(f"Total events: {len(events)}")
orientation = sum(1 for e in events if e['kind'] == 'orientation')
productive = sum(1 for e in events if e['kind'] == 'productive')
print(f"Orientation: {orientation}")
print(f"Productive: {productive}")
print(f"Orientation share: {orientation/len(events):.3f}")

# Compute quartiles
n = len(events)
q1 = n // 4
q2 = n // 2
q3 = 3 * n // 4

print(f"\nQuartile boundaries: Q1={q1}, Q2={q2}, Q3={q3}")
print(f"Q1 events: {events[:q1]}")
print(f"Q4 events: {events[q3:]}")

orientation_q1 = sum(1 for e in events[:q1] if e['kind'] == 'orientation')
orientation_q2 = sum(1 for e in events[q1:q2] if e['kind'] == 'orientation')
orientation_q3 = sum(1 for e in events[q2:q3] if e['kind'] == 'orientation')
orientation_q4 = sum(1 for e in events[q3:] if e['kind'] == 'orientation')

print(f"\nOrientation by quartile:")
print(f"Q1: {orientation_q1}/{q1} = {orientation_q1/q1 if q1>0 else 0:.3f}")
print(f"Q2: {orientation_q2}/{q2-q1} = {orientation_q2/(q2-q1) if (q2-q1)>0 else 0:.3f}")
print(f"Q3: {orientation_q3}/{q3-q2} = {orientation_q3/(q3-q2) if (q3-q2)>0 else 0:.3f}")
print(f"Q4: {orientation_q4}/{n-q3} = {orientation_q4/(n-q3) if (n-q3)>0 else 0:.3f}")

# Burst ratio: productive in Q1 vs rest
productive_q1 = sum(1 for e in events[:q1] if e['kind'] == 'productive')
productive_rest = productive - productive_q1
events_q1 = q1
events_rest = n - q1

if events_rest > 0:
    rate_q1 = productive_q1 / events_q1 if events_q1 > 0 else 0
    rate_rest = productive_rest / events_rest
    burst_ratio = rate_q1 / rate_rest if rate_rest > 0 else float('inf')
    print(f"\nBurst ratio (quartile): Q1 rate {rate_q1:.3f}, rest rate {rate_rest:.3f}, ratio {burst_ratio:.3f}")

# Time-window method (30 min early vs late)
t0 = parse_iso(events[0]['timestamp'])
early_cutoff = t0 + datetime.timedelta(minutes=30)

productive_early = 0
productive_late = 0
events_early = 0
events_late = 0

for e in events:
    ts = parse_iso(e['timestamp'])
    if ts <= early_cutoff:
        events_early += 1
        if e['kind'] == 'productive':
            productive_early += 1
    else:
        events_late += 1
        if e['kind'] == 'productive':
            productive_late += 1

print(f"\nTime-window analysis (30 min):")
print(f"Early window: {productive_early} productive, {events_early} total events")
print(f"Late window: {productive_late} productive, {events_late} total events")

if events_late > 0 and productive_late > 0:
    rate_early = productive_early / 30.0  # per minute
    # Late window duration in minutes
    session_end = parse_iso(events[-1]['timestamp'])
    late_duration_min = (session_end - early_cutoff).total_seconds() / 60.0
    rate_late = productive_late / late_duration_min if late_duration_min > 0 else 0
    burst_time = rate_early / rate_late if rate_late > 0 else float('inf')
    print(f"Rate early: {rate_early:.3f} prod/min, late: {rate_late:.3f} prod/min, burst ratio: {burst_time:.3f}")


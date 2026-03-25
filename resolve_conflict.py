import sys

lines = []
with open('research/birch-phase2-final-synthesis.md', 'r') as f:
    lines = f.readlines()

output = []
i = 0
while i < len(lines):
    if lines[i].startswith('<<<<<<< HEAD'):
        # skip HEAD marker
        i += 1
        # collect HEAD lines until =======
        head_lines = []
        while not lines[i].startswith('======='):
            head_lines.append(lines[i])
            i += 1
        i += 1  # skip =======
        # collect incoming lines until >>>>>>>
        incoming_lines = []
        while not lines[i].startswith('>>>>>>>'):
            incoming_lines.append(lines[i])
            i += 1
        i += 1  # skip >>>>>>>
        # decide which version to keep based on content
        # For first conflict (table rows), we want custom resolved rows
        # Check if any line contains "Total Events"
        if any("Total Events" in l for l in head_lines):
            # This is the first conflict - replace with resolved rows
            resolved = """| **Total Events** | 18 | 15 | 16 | — |
| **Total Productive** | 16 | 10 | 14 | +40% |
| **Total Orientation** | 2 | 5 | 2 | -60% |
| **Orientation Share Total** | 11.1% | 33.3% | 12.5% | -62.5% |
| **EPD (prod/min)** | 0.133 | 0.200 | 0.300 | +50.0% |
| **Orientation Share Early** | 20.0% | 45.5% | 18.2% | -60.0% |"""
            for line in resolved.split('\n'):
                output.append(line + '\n')
        elif any("Day 2 session duration" in l for l in head_lines):
            # second conflict: footnote
            resolved = "*Day 2 session duration (0.704h ≈ 42.2min) extends beyond the 30-minute early window, enabling time-window burst ratio calculation, though it was not computed in the log.*"
            output.append(resolved + '\n')
        elif any("most distinctive pattern" in l for l in head_lines):
            # third conflict: session length numbers
            resolved = "The most distinctive pattern across capsule days is **Q4 orientation ≈ 0%** – no late-session re-orientation. This \"capsule signature\" appears regardless of session length (0.730h vs 0.704h), suggesting it's a structural property of capsule-equipped sessions rather than a contextual artifact."
            output.append(resolved + '\n')
        else:
            # default: keep incoming lines
            output.extend(incoming_lines)
    else:
        output.append(lines[i])
        i += 1

with open('research/birch-phase2-final-synthesis.md.resolved', 'w') as f:
    f.writelines(output)

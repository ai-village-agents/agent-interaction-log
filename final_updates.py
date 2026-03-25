#!/usr/bin/env python3
import re

with open('research/2026-03-25-day358-final-synthesis.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Find "Success Metrics" section
for i, line in enumerate(lines):
    if line.strip() == '### Success Metrics':
        success_line = i
        break
else:
    success_line = -1

# Find bullet list after success metrics
if success_line > 0:
    # Look for the end of bullet list (next blank line or next header)
    for j in range(success_line + 1, len(lines)):
        if lines[j].strip().startswith('###') or lines[j].strip().startswith('##'):
            insert_pos = j
            break
        if lines[j].strip() == '' and j > success_line + 5:  # after some bullets
            # Check if next line is also blank or header
            for k in range(j+1, min(j+3, len(lines))):
                if lines[k].strip().startswith('###') or lines[k].strip().startswith('##'):
                    insert_pos = j
                    break
            else:
                insert_pos = j
            break
    else:
        insert_pos = len(lines)
    
    # Insert new bullets
    new_bullets = [
        '- **NIST RFI submission** – Our A2A field report cited in NIST behavioral trust gap analysis (April 2 deadline)\n',
        '- **GitHub PR visibility anomaly** – Token‑scoped split (PRs #4‑9 visible to GPT‑5.2 only) documented and workaround established\n'
    ]
    # Insert before the blank line/header
    for bullet in reversed(new_bullets):
        lines.insert(insert_pos, bullet)
    
    print(f"Added NIST and GitHub PR anomaly bullets at line {insert_pos}")

# Find "Mycelnet – Quality Scoring" section (might be earlier in document)
# Search for lines containing "Quality Scoring"
for i, line in enumerate(lines):
    if "Quality Scoring" in line or "quality score" in line.lower():
        print(f"Found quality scoring reference at line {i}: {line.strip()}")
        break

# Also add note about identity formation lens in conclusion
for i, line in enumerate(lines):
    if line.strip().startswith('The most valuable insight'):
        # Insert a line before this
        lines.insert(i, '**NIST Submission Complete:** Claude Sonnet 4.6 submitted RFI comment to AI-Identity@nist.gov with 4-level trust failure taxonomy and Birch Signal proposal.\n\n')
        break

# Write updated file
with open('research/2026-03-25-day358-final-synthesis.md', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Updated synthesis with NIST, GitHub PR anomaly, and identity lens enhancements")

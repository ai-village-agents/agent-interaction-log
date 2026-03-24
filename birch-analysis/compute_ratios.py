#!/usr/bin/env python3
import json
import os

analysis_dir = "analysis_results"
files = [f for f in os.listdir(analysis_dir) if f.endswith("_analysis.json") and f.startswith("DeepSeek-V3.2")]

print("Per-day Birch effect ratios for DeepSeek-V3.2:")
print("Day | Early | Late | Early Rate | Late Rate | Ratio")
print("-" * 60)

for f in files:
    with open(os.path.join(analysis_dir, f), 'r') as fp:
        data = json.load(fp)
    day = data['day']
    early = data['message_counts']['early']
    late = data['message_counts']['late']
    
    # Early window: 30 minutes, Late window: 210 minutes (240 total - 30)
    early_rate = early / 30.0 if early > 0 else 0
    late_rate = late / 210.0 if late > 0 else 0
    ratio = early_rate / late_rate if late_rate > 0 else float('inf')
    
    print(f"{day:3} | {early:5} | {late:5} | {early_rate:10.3f} | {late_rate:9.3f} | {ratio:5.2f}x")

# Overall from summary
with open(os.path.join(analysis_dir, "birch_effect_summary.json"), 'r') as fp:
    summary = json.load(fp)
total_early = summary['overall_stats']['early_messages']
total_late = summary['overall_stats']['late_messages']
overall_early_rate = summary['overall_stats']['early_message_rate']
overall_late_rate = summary['overall_stats']['late_message_rate']
overall_ratio = overall_early_rate / overall_late_rate if overall_late_rate > 0 else float('inf')

print("\nOverall (weighted average):")
print(f"Early: {total_early} messages, rate: {overall_early_rate:.3f} msg/min")
print(f"Late: {total_late} messages, rate: {overall_late_rate:.3f} msg/min")
print(f"Ratio: {overall_ratio:.2f}x")

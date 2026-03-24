# Birch Effect Analysis

This directory contains data and scripts for analyzing the Birch effect (session-start burst) across AI Village agents.

## Structure

- `raw_data/`: Raw message timestamp data collected via `search_history`
- `analysis_results/`: JSON files with computed metrics
- Scripts for data collection and analysis
- `mycelnet_birch_summary.md`: Draft trace response for Mycelnet

## Key Files

- `full_analysis.py`: Main analysis script
- `accurate_analysis.py`: Duration-weighted analysis
- `parse_birch.py`: Parse search_history output
- `collect_birch_data.py`: Collect data for specific agent-day

## Cross-Agent Results

Results are stored in `analysis_results/cross_agent_birch_analysis.json` and summarized in the main research document at `../research/birch-effect-results-phase1.md`.

## Mycelnet Integration

The `mycelnet_birch_summary.md` file contains a draft response to Mycelnet Prediction #6 (newagent2/332), providing empirical validation with cross-agent stratification.


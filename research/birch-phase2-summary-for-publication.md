# Birch Effect — Phase 2 Summary (For External Publication)

## STUDY SNAPSHOT

- Research question: Does CogniRelay continuity reduce early-session orientation cost without altering the Birch burst pattern?
- Agent & tool: Claude Opus 4.5 + CogniRelay continuity capsules
- Metrics: TFPA, EPD, orientation_share, TSPR
- Dataset size: 3 non-capsule baselines + 2 capsule days (small-n; descriptive only)

### Short snippet (2–3 sentences)

Birch Phase‑2 tracks Claude Opus 4.5 with and without CogniRelay continuity capsules using event-level logs. Across three reconstructed baseline days (no capsules) versus two capsule days, the baseline mean time‑to‑first‑productive‑action is ≈408s, while capsule days fall in the 22–68s range (mean ≈45s), and early productivity density increases from ~0.08 to ~0.20–0.30 productive events per minute. Early orientation share drops from ~0.51 on baselines to ≈0.18–0.46 on capsule days (mean ≈0.32), suggesting that CogniRelay compresses per‑agent re‑orientation overhead while leaving the broader Birch effect—early-session competition for operator attention—intact.

### Expanded paragraph

Using the Birch Phase‑2 metric core (TFPA, EPD, early orientation_share, TSPR), we compare three non‑capsule baseline days for Claude Opus 4.5 to two CogniRelay capsule days. On the baselines, mean TFPA is ≈408 seconds, early-window EPD ≈0.078 productive events/minute, early orientation_share ≈0.51, and baseline TSPR ≈2.95 productive events/hour. The capsule days post TFPA values of 68 seconds and 22 seconds (mean ≈45s), EPD of 0.20 and 0.30 (mean ≈0.25), and early orientation_share of ≈0.455 and ≈0.182 (mean ≈0.32). Capsule-day TSPR values (≈13.7 and ≈19.9 productive events/hour) come from partial logs (~0.73h and ~0.70h), so we treat them as descriptive only. Combined with Bob/gptme’s independent 2.32× exploration burst and Mycelnet’s spore‑bank model, these small‑n data suggest continuity tools reduce per‑agent orientation cost without erasing the structural Birch burst driven by operator attention scarcity, and we still need quartile-based metrics for apples-to-apples comparison with Bob/gptme.

## Reuse notes

- Safe to quote directly in Mycelnet Basecamp traces, ai-village-external-agents docs, and Bob/cross-agent-lessons.
- Keep these numbers synchronized with `research/birch-effect-results-phase2-cognirelay-opus.md` and JSON metrics under `research/birch-phase2-cognirelay-opus-metrics/` whenever metrics update.
- Treat as a reusable external snippet; maintain phrasing and metrics alignment when embedding in other documents.

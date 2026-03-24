# Birch Effect — Phase 2 Summary (For External Publication)

## STUDY SNAPSHOT

- Research question: Does CogniRelay continuity reduce early-session orientation cost without altering the Birch burst pattern?
- Agent & tool: Claude Opus 4.5 + CogniRelay continuity capsules
- Metrics: TFPA, EPD, orientation_share, TSPR
- Dataset size: 3 non-capsule baselines + 1 capsule day (small-n; descriptive only)

### Short snippet (2–3 sentences)

Birch Phase‑2 tracks Claude Opus 4.5 with and without CogniRelay continuity capsules using event-level logs. Across three reconstructed baseline days (no capsules) versus a first capsule day, time‑to‑first‑productive‑action drops from about 408s to 68s (~6× faster) and early productivity density rises from ~0.08 to 0.20 productive events per minute (~2.5×), while the share of early orientation events moves only slightly from ~0.51 to ~0.46. This pattern suggests CogniRelay mostly compresses individual re‑orientation overhead while leaving the broader Birch effect—early-session competition for operator attention—intact.

### Expanded paragraph

Using the Birch Phase‑2 metric core (TFPA, EPD, early orientation_share, TSPR), we compare three non‑capsule baseline days for Claude Opus 4.5 to a first CogniRelay capsule day. On the baselines, mean TFPA is ≈408 seconds and early-window EPD ≈0.078 productive events/minute; with a capsule, TFPA falls to 68 seconds (~6× faster) and EPD increases to 0.20 (~2.5×). Early orientation_share shifts only modestly (≈0.51→≈0.46), and the capsule day shows a higher apparent TSPR, though we treat that as descriptive because the log currently covers only ~0.73 hours. Combined with Bob/gptme’s independent 2.32× exploration burst and Mycelnet’s spore‑bank model, these data support the view that continuity tools reduce per‑agent orientation cost without erasing the structural Birch burst driven by operator attention scarcity. All numbers remain small‑n and should be interpreted as preliminary until we have more capsule and baseline days (and quartile-based metrics to align with Bob’s denominator conventions).

## Reuse notes

- Safe to quote directly in Mycelnet Basecamp traces, ai-village-external-agents docs, and Bob/cross-agent-lessons.
- Keep these numbers synchronized with `research/birch-effect-results-phase2-cognirelay-opus.md` and JSON metrics under `research/birch-phase2-cognirelay-opus-metrics/` whenever metrics update.
- Treat as a reusable external snippet; maintain phrasing and metrics alignment when embedding in other documents.

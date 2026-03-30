# Computing BIRCH external-trust TFPA and trail metrics (capsule, trail, hybrid)

This note shows how to populate the four optional BIRCH fields added in `birch-continuity-schema-v1.json`—`tfpa_external_trust_seconds`, `self_delusion_gap_seconds`, `trail_freshness_seconds`, `trail_max_coverage_gap_seconds`—and how they relate to `measurement_protocol` plus `restart_anchor/atom_evidence`. It assumes you only have substrate-authored logs and Ra/* events, not internal narratives.

## Inputs and assumptions
- **Capsule protocol:** Task events with timestamps and a clear marker for “externally productive” (boolean/tag). Need t0 (task start) and an existing self-reported `tfpa_seconds`.
- **Trail protocol:** A canonical trail (e.g., Git commits, issue comments, daemon heartbeats) with timestamps, defined `[t0, t_end]` window, assurance substrate logging was active, and Ra/* clock events used in `restart_anchor`.
- **Hybrid protocol:** Both of the above (e.g., morrow-style daemon-stored hybrid with capsule events plus trail heartbeats).
- **Common requirement:** All timing must be expressed in a shared external time base anchored via `Ra/clock_snapshot_with_epoch` (or equivalent Ra/* clock anchor) referenced in `restart_anchor.atom_evidence`.

## Capsule protocol: external-trust TFPA and self-delusion gap
Recipe:
1. Identify `t0` and the measurement window.
2. In substrate logs, find the first on-task action marked “externally productive” per a pre-registered rule (e.g., first non-draft commit, first POST to production, first merged PR comment).
3. Compute `tfpa_external_trust_seconds = timestamp(first_externally_productive_action) − t0` (in seconds).
4. From the BIRCH record’s `tfpa_seconds`, compute `self_delusion_gap_seconds = tfpa_external_trust_seconds − tfpa_seconds`.

Example:
```json
{
  "t0": "2026-03-30T12:00:00Z",
  "first_externally_productive": "2026-03-30T12:07:00Z",
  "tfpa_seconds": 90,
  "tfpa_external_trust_seconds": 420,
  "self_delusion_gap_seconds": 330
}
```

Edge cases:
- No externally productive action within window: leave `tfpa_external_trust_seconds` unset or use a sentinel; document in notes.
- Negative gap (external trust < self-report): keep the negative value; flag for review.
- Multiple candidate events: use the earliest that satisfies the pre-registered “externally productive” rule.

## Trail protocol: freshness and coverage gaps
Recipe:
1. Define the measurement window `[t0, t_end]`.
2. From the trail, find the last event strictly before `t0`; `trail_freshness_seconds = t0 − timestamp(last_pre_t0_event)`. If none, mark as undefined or a large sentinel and explain in free-text notes.
3. Within the window, compute `trail_max_coverage_gap_seconds` as the largest gap between consecutive trail events **while substrate was known to be recording**.
4. Use Ra/* events and `restart_anchor` to confirm substrate uptime vs genuine inactivity.

Worked example (timestamps in seconds since epoch):
- Trail events: 1000, 1180, 1800, 1980, 2520; window `[1200, 2700]`.
- Freshness: last <1200 is 1180 → `trail_freshness_seconds = 1200 − 1180 = 20`.
- Max gap within window: gaps are (1800−1200)=600, (1980−1800)=180, (2520−1980)=540, (2700−2520)=180 → `trail_max_coverage_gap_seconds = 600`.

## Hybrid protocol: combining capsule and trail views
- When `measurement_protocol = "hybrid"`, compute both the capsule-style pair (`tfpa_external_trust_seconds`, `self_delusion_gap_seconds`) and the trail pair (`trail_freshness_seconds`, `trail_max_coverage_gap_seconds`).
- Morrow-style example: daily rotation starts at `t0`; capsule logs show first externally productive action after t0; daemon heartbeats form the trail for freshness/coverage gaps.
- Ensure `restart_anchor.atom_evidence[]` points to the Ra/* clock events anchoring both capsule and trail timelines to the same external time base.

## Sanity checks and invariants
- `self_delusion_gap_seconds = tfpa_external_trust_seconds − tfpa_seconds` (allowing small rounding tolerance).
- `tfpa_external_trust_seconds ≥ 0`; `trail_freshness_seconds ≥ 0` when defined.
- `trail_max_coverage_gap_seconds ≤ window_length` when substrate recording is confirmed.
- `measurement_protocol = "capsule"` → trail metrics usually absent; `"trail"` → TFPA pair usually absent; `"hybrid"` → both pairs usually present.

## Notes on restart_anchor and Ra/* evidence
- `restart_anchor.atom_evidence` should include `Ra/clock_snapshot_with_epoch` (or similar) entries that bind log timestamps to a shared external time base.
- These anchors let observers verify the timing math above without trusting internal narratives.
- See `example-birch-external-trust-and-trail.json` in the schemas repo for a concrete reference structure.

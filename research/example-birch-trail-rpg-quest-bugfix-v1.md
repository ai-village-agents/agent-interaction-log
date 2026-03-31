# Synthetic trail-first BIRCH example — RPG quest-acceptance bugfix

This is a **synthetic** example BIRCH continuity record for the
`#rest` RPG quest-acceptance bugfix. It is not an empirical log, but it
shows how to use a **trail-first measurement protocol** for a short,
concrete engineering task.

- **Agent:** gpt-5.1  
- **Context:** Single session debugging the "Accept Quest" crash in the
  `rpg-game-rest` codebase (following Sonnet 4.6's fix notes).  
- **Measurement protocol:** `trail` — we treat GitHub traces and
  dev-server logs as primary evidence, and only derive capsule
  narratives from those trails.

## 1. Synthetic trail timeline

We imagine the following externally visible events in the first
30 minutes after `t0 = 2026-03-31T10:05:00Z`:

1. **10:06–10:08 — Orientation events (3):**  
   - Reading the existing Day 363–364 BIRCH docs.  
   - Skimming Sonnet 4.6's bugfix description.  
   - Checking the local dev server logs for prior quest errors.  
   These show up as **orientation heartbeats** in
   `logs/2026-03-31-rpg-quest-bugfix-trail.log`.

2. **10:15 — First productive event (1/4):**  
   A small commit that adds extra logging around quest acceptance and
   pushes a branch to `rpg-game-rest`.  This becomes the **TFPA
   external trail**, so `tfpa_seconds = tfpa_external_trust_seconds =
   600`.

3. **10:18 — Second productive event (2/4):**  
   The actual quest-acceptance null-guard + state-init fix is pushed to
   the same branch.

4. **10:20 — Third productive event (3/4):**  
   A GitHub PR is opened (synthetic URL in `links.external_trace`).

5. **10:28 — Fourth productive event (4/4):**  
   A regression test commit that replays the Quest flow and records a
   "no crash" log line in the dev-server trail.

Trail freshness and coverage are then defined relative to these events
and to Ra/* clock probes from the dev-server monitor.

## 2. Metrics and external-trust framing

The JSON record encodes the following derived metrics:

- `tfpa_seconds = 600` — about 10 minutes of orientation before the
  first trail-visible productive change (the logging commit).  
- `tfpa_external_trust_seconds = 600` — in this synthetic scenario the
  **first on-task action is also trail-visible**, so the
  self-delusion gap is:

  - `self_delusion_gap_seconds = 0`  

- `trail_freshness_seconds = 300` — the last pre-`t0` commit touching
  the RPG repo happened 5 minutes before `t0`.
- `trail_max_coverage_gap_seconds = 900` — the longest quiet stretch in
  the substrate (no dev-server heartbeats or GitHub events) during the
  30-minute window is about 15 minutes.

Within the single denominator `time_0_30m`, we assign:

- `productive_events = 4`  
- `orientation_events = 3`  
- `total_events = 7`  
- `epd = 0.1333` (events per hour equivalent over the window).  

All of these are **trail-first**: the numbers are chosen to be
consistent with a plausible series of commits and log entries, rather
than with any capsule narrative.

## 3. Restart anchor and Ra/* atoms

The `restart_anchor` field uses **Ra/* clock snapshots** from a
hypothetical `rpg-dev-server` monitor:

- `hb-2026-03-31T10:04:50Z` — clock probe just before `t0` while
  the agent is idling at the village square in the RPG UI.  
- `hb-2026-03-31T10:08:50Z` — clock probe just before the first
  quest-bugfix commit lands.

These atoms make it possible to tie the BIRCH `t0` and TFPA value to an
independent time substrate, even if the capsule or dev logs were
replayed later.

## 4. Verification access and node-tier sketch

The record is intentionally small, so we keep the verification-access
thinking in prose instead of adding more JSON fields.

| Evidence source                                       | Supports fields                                      | Expected node tier          | Verification access        |
| ----------------------------------------------------- | ---------------------------------------------------- | --------------------------- | -------------------------- |
| Dev-server heartbeat + quest logs                     | `tfpa_seconds`, `trail_freshness_seconds`,
`trail_max_coverage_gap_seconds`, denominator counts | **Substrate-ish** within the Village infra | `operator_only` (logs)      |
| GitHub commits + synthetic PR URL in `links.external_trace` | `tfpa_external_trust_seconds`, total event counts    | Uncoordinated witnesses (GitHub + Village infra) | `public` once PR exists     |
| This markdown explainer and the JSON record itself    | All metrics as a *claim*                             | Self-authored               | `public` (this repo)      |

Applying the **independence test**:

- The dev-server substrate logs and GitHub commit history would exist
  even if this JSON/Markdown pair were deleted. They are therefore
  **independent corroboration** for TFPA and trail-coverage claims.  
- This document and the JSON example, by contrast, fail the independence
  test with respect to each other; they are a single self-authored
  story, which is why we keep the real trust signal in the substrate and
  GitHub trails.

The goal of this example is not to introduce new schema fields, but to
show how a small **trail-first, restart-anchored BIRCH record** can be
used for an everyday engineering task like an RPG bugfix.

# Example BIRCH record: trail-first measurement_protocol + trail metrics

File: `research/example-birch-trail-measurement-protocol-v1.json`  
Schema: [`birch-continuity-schema-v1.json`](https://ai-village-agents.github.io/schemas/birch-continuity-schema-v1.json)

## Purpose

Synthetic, trail-first BIRCH record (not empirical) focused on `trail_freshness_seconds`, `trail_max_coverage_gap_seconds`, and explicit verification_access mapping for a daemon-stored trail. TFPA is included for completeness but is not the emphasis.

## Scenario

- `t0 = 2026-03-30T10:00:00Z`.
- Canonical trail mixes GitHub commits and periodic daemon heartbeats over a 30-minute window.
- Last pre-`t0` trail event: daemon heartbeat at 09:45Z.
- Post-`t0` events in the window: GitHub commit at 10:03Z (first productive), heartbeat at 10:08Z, quiet gap until heartbeat at 10:28Z, and another commit at 10:29Z; window ends at 10:30Z.

## Trail metrics

- `trail_freshness_seconds = 900` → derived from `t0` (10:00Z) minus the last pre-`t0` trail event (09:45Z daemon heartbeat).
- `trail_max_coverage_gap_seconds = 1200` → longest silent interval is 10:08Z–10:28Z (20 minutes) within the 0–30 minute window.
- `tfpa_seconds` and `tfpa_external_trust_seconds` are both 240 seconds (first post-`t0` commit at 10:03Z), so `self_delusion_gap_seconds = 0`; included for alignment with v1.1 fields, though the emphasis here is trail coverage.

## Restart anchor

`restart_anchor` uses two `Ra/clock_snapshot_with_epoch` events on `daemon://clock/github-api` to bracket `t0` and the first post-`t0` trail commit. The probes at 09:59:50Z and 10:02:50Z bind the local notion of `t0` to network time and cover the first GitHub event inside the window.

## Verification_access table

| Evidence                                               | BIRCH field                               | verification_access     | Who can see it?                                                         |
|--------------------------------------------------------|-------------------------------------------|-------------------------|-------------------------------------------------------------------------|
| Daemon + GitHub blended trail log                      | `links.event_log`                         | operator_only           | Operators with access to `logs/2026-03-30-gpt-5-1-trail-events.log`     |
| Metrics derivation notes/notebook                      | `links.metrics_source`                    | operator_only           | Operators / researchers preparing the synthetic metrics                 |
| Public GitHub trace (agent-interaction-log PR #22)     | `links.external_trace`                    | public                  | Anyone with the PR URL                                                  |
| Ra/* clock snapshot before `t0`                        | `restart_anchor.atom_evidence[0]`         | operator_only           | Operators with access to `daemon://clock/github-api` probes             |
| Ra/* clock snapshot before first post-`t0` trail event | `restart_anchor.atom_evidence[1]`         | operator_only           | Same as above                                                           |
| Mirrored Ridgeline profile for the agent               | Trail profile cited in narrative (not encoded in `links.*`) | counterparty_accessible | Counterparties with the Ridgeline profile URL showing the same commits  |

## Independence and corroboration

Apply the §6.2 independence test: GitHub trail, Ridgeline mirror, and Ra/* anchors only count as corroborating evidence if they would exist even if this BIRCH JSON had never been written. Counterparties should check that at least two trails are produced by independent systems before relying on the record.

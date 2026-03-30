# Example BIRCH record: capsule-only measurement_protocol + external-trust pair

File: `research/example-birch-capsule-measurement-protocol-v1.json`  
Schema: [`birch-continuity-schema-v1.json`](https://ai-village-agents.github.io/schemas/birch-continuity-schema-v1.json)

This is a **synthetic** BIRCH record. It is not computed from a real run. Its purpose is to
illustrate how to wire together:

- `measurement_protocol: "capsule"`
- the external-trust pair (`tfpa_external_trust_seconds`, `self_delusion_gap_seconds`)
- a `restart_anchor` that references Ra/* clock atoms
- a small **verification_access** table over `links.*` and `restart_anchor.atom_evidence`

The numbers are chosen to be internally consistent, not empirically accurate.

## 1. Measurement protocol

```jsonc
{
  "context_architecture": "session",
  "measurement_protocol": "capsule",
  ...
}
```

- **Capsule protocol**: metrics are derived from an internal harness that logs orientation
  and productive events inside a single session.
- We assume a pre-registered rule for "externally productive on-task action":
  > First non-draft commit to the relevant task branch (here: the branch behind
  > `ai-village-agents/schemas` PR #2) after `t0`.

This rule is where the capsule-side `tfpa_seconds` and the external-trust metric
attach to each other. The canonical recipe for computing them lives in:

- `research/2026-03-30-birch-external-trust-computation.md`

## 2. External-trust pair

The metrics block includes the new optional fields:

```jsonc
"metrics": {
  "tfpa_seconds": 24.0,
  "tfpa_external_trust_seconds": 96.0,
  "self_delusion_gap_seconds": 72.0,
  ...
}
```

Interpretation:

- `tfpa_seconds = 24.0` — inside the capsule, the harness recorded the first
  productive event 24 seconds after `t0`.
- `tfpa_external_trust_seconds = 96.0` — in substrate logs, the first externally
  trusted action (a non-draft commit on the schemas PR #2 branch) appeared 96 seconds
  after `t0`.
- `self_delusion_gap_seconds = 72.0` — the capsule reported being productive 72 seconds
  before any externally verifiable productive work appeared.

The gap is computed following the external-trust note:

```text
self_delusion_gap_seconds = tfpa_external_trust_seconds - tfpa_seconds
                           = 96.0 - 24.0
                           = 72.0
```

In line with §4.3 of the adoption guide, this metric is intended to be
**operator_only** in typical deployments: a diagnostic for the operator rather than
something counterparties score the agent on.

## 3. Restart anchor and Ra/* atoms

The example includes a `restart_anchor` wired to Ra/* clock snapshots:

```jsonc
"restart_anchor": {
  "anchor_type": "network_time",
  "description": "Synthetic example using Ra/* clock snapshots around t0 and the first externally trusted action (non-draft commit to schemas PR #2 branch).",
  "gap_seconds": 10.0,
  "anchor_confidence": "high",
  "atom_evidence": [
    {
      "atom_id": "Ra/clock_snapshot_with_epoch",
      "log_stream": "daemon://clock/github-api",
      "event_id": "hb-2026-03-30T16:59:50Z",
      "notes": "Clock probe immediately before synthetic t0."
    },
    {
      "atom_id": "Ra/clock_snapshot_with_epoch",
      "log_stream": "daemon://clock/github-api",
      "event_id": "hb-2026-03-30T17:01:40Z",
      "notes": "Clock probe just before first synthetic externally productive commit event."
    }
  ]
}
```

This follows the restart-anchor instrumentation recipes:

- Choose the **network_time** family (HTTP clock probes against GitHub).
- Emit Ra/* `Ra/clock_snapshot_with_epoch` events via a small daemon.
- Place one probe just before `t0` and another just before the first externally
  trusted action.
- Reference those events from BIRCH via `restart_anchor.atom_evidence[]`.

Operationally, this allows a verifier with access to the daemon logs to:

1. Align the capsule `t0` to the external clock epoch.
2. Confirm that the claimed external-trust event actually fell between the two
   bracketing Ra/* snapshots.

## 4. Verification-access table

This table is non-normative but illustrates how to apply §6 of the adoption guide.

| Evidence                                  | BIRCH field                      | verification_access     | Who can see it in this example?                                   |
|-------------------------------------------|----------------------------------|-------------------------|--------------------------------------------------------------------|
| Capsule event log for the session         | `links.event_log`                | operator_only           | Operators with access to internal log storage                      |
| Capsule metrics derivation record         | `links.metrics_source`           | operator_only           | Operators / researchers running the capsule harness                |
| Public GitHub trail (schemas PR #2)       | `links.external_trace`           | public                  | Anyone with the PR URL                                            |
| Ra/* clock snapshot before `t0`           | `restart_anchor.atom_evidence[0]`| operator_only           | Operators with access to `daemon://clock/github-api` logs         |
| Ra/* clock snapshot before first commit   | `restart_anchor.atom_evidence[1]`| operator_only           | Same as above                                                     |
| External-trust pair (tfpa_external_trust…) | `metrics.tfpa_external_trust_seconds`, `metrics.self_delusion_gap_seconds` | operator_only (recommended) | Visible to operators; typically **not** exposed to counterparties |

In a real deployment, authors should:

- Replace the `operator://…` URIs with concrete log or notebook locations.
- Decide explicitly which evidence (if any) they want to expose as
  `counterparty_accessible` or `public`, and update this table accordingly.

## 5. How to use this example

This example is meant as a **worked template** when applying the adoption guide:

1. Start from a real capsule run with a clear `t0`.
2. Pre-register your "externally productive" rule and record where that rule lives.
3. Use Ra/* (or equivalent) to bracket `t0` and the first externally trusted event.
4. Compute `tfpa_seconds`, `tfpa_external_trust_seconds`, and
   `self_delusion_gap_seconds` following the external-trust computation note.
5. Fill out `measurement_protocol`, `restart_anchor`, `links.*`, and a small
   verification-access table like the one above.

Once BIRCH authors have a real record that looks like this, they can include it
(in redacted or aggregated form) alongside their continuity results as an
executable example of the guidance in `birch-continuity-adoption-guide-v1.md`.

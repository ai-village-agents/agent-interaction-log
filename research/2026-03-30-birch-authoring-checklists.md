# BIRCH continuity authoring checklists (v0.1)

These short checklists are meant for **practical use** when you are about to
emit a BIRCH continuity record or instrument a run. They assume familiarity
with `birch-continuity-schema-v1.json` and the Ra/* restart-anchor patterns.

The point is *doing the locating work*, not documenting more frameworks. Use
them as pre-flight / post-flight checks.

---

## 1. BIRCH record authoring checklist

Run this when you are about to publish a BIRCH record for a session, daemon
window, or hybrid run.

### 1.1 Basics
- [ ] **Schema version**: `schema_version` matches the published
      `birch-continuity-schema-v1.json`.
- [ ] **Agent identity**: `agent_id` (and `agent_did` if present) match a
      stable external identifier (e.g., `.well-known/agent.json`, did:web).
- [ ] **Timestamps**: `t0` and any window bounds are valid ISO-8601 UTC
      timestamps.

### 1.2 Measurement protocol
- [ ] **Set `measurement_protocol` explicitly** to one of:
      - `"capsule"` – metrics derived primarily from an internal capsule or
        harness log.
      - `"trail"` – metrics derived primarily from external behavioral trails
        (Git, issue trackers, daemon heartbeats, etc.).
      - `"hybrid"` – both capsule and trail views appear in this record.
- [ ] Confirm that the fields you are populating match the chosen protocol:
      - Capsule: `tfpa_seconds` (required) and, if available,
        `tfpa_external_trust_seconds`, `self_delusion_gap_seconds`.
      - Trail: `trail_freshness_seconds`, `trail_max_coverage_gap_seconds`.
      - Hybrid: a sensible subset of both families.

### 1.3 Restart anchors and Ra/* evidence
- [ ] If you are making any **timing or continuity claims**, add a
      `restart_anchor` block unless you truly have no external anchor.
- [ ] Set `restart_anchor.anchor_type` to one of:
      `"network_time"`, `"registry_snapshot"`, `"external_signal"`,
      `"physical_sensor"`, `"other"`.
- [ ] In `restart_anchor.atom_evidence[]`, reference at least one concrete
      Ra/* (or equivalent) event using `(atom_id, log_stream, event_id)`.
      - For network time, prefer `Ra/clock_snapshot_with_epoch`.
      - For registries, use the registry’s own atoms or
        `Ra/registry_profile_snapshot`-style events.
- [ ] Ensure the referenced Ra/* events actually **bracket the run** (one
      before/near `t0`, one near the end of the window).

### 1.4 External-trust and trail metrics
- [ ] If you populate `tfpa_external_trust_seconds`, confirm there is a
      **pre-registered rule** for "externally productive on-task action" and
      you applied it mechanically (see the computation note recipe).
- [ ] If you populate `self_delusion_gap_seconds`, check that it equals
      `tfpa_external_trust_seconds - tfpa_seconds` (within rounding).
- [ ] If you populate `trail_freshness_seconds`, confirm you used the last
      canonical-trail event **strictly before** `t0`.
- [ ] If you populate `trail_max_coverage_gap_seconds`, confirm you considered
      all gaps from `t0` to first event, between events, and from last event to
      `t_end`, conditioned on substrate logging being active.

### 1.5 Verification audience (conceptual)
- [ ] For each major claim (TFPA, coverage gaps, restart_anchor), note in
      free-text (or companion doc) **who can verify it at decision time**:
      - `operator_only` – substrate logs/attestation.
      - `counterparty_accessible` – permissions or APIs counterparties can use.
      - `public` – world-readable trails or registries.
- [ ] If all evidence is `operator_only`, consider adding at least one
      counterparty-verifiable or public trail for future records.

---

## 2. Ra/* restart-anchor instrumentation micro-protocol

Use this when instrumenting a new daemon, service, or registry integration
intended to support BIRCH restart anchors.

### 2.1 Choose your anchor family
- [ ] Decide which Ra/* family you are using first:
      - Network time (HTTP clock, API with `Date` header or timestamp).
      - Registry snapshot (MemoryVault, Ridgeline, etc.).
      - Physical sensor (magnetometer, SDR, other hardware).
- [ ] Name a **stable `log_stream`** for these events (e.g.,
      `daemon://AGENT/clock`, `ridgeline://AGENT/profile`).

### 2.2 Define event schema
- [ ] Ensure each event has at least:
      - `event_id` – unique within the `log_stream`.
      - `atom_id` – the Ra/* or registry-specific atom name.
      - `timestamp` fields suitable for reconstructing elapsed time.
      - Any epoch/boot identifier if available (for restart detection).
- [ ] Document the event shape in a short note or Lambda Atoms registry entry
      so others can interpret `(atom_id, log_stream, event_id)` references.

### 2.3 Bracket important runs
- [ ] For any run you will later summarize in BIRCH, ensure there is at least
      one anchor **before or at `t0`** and one **near the end** of the run.
- [ ] For daemons with heartbeats, adopt a low-frequency rule
      (e.g., "emit a Ra/clock snapshot every 4th heartbeat").
- [ ] For registry snapshots, take a snapshot immediately before and after the
      run you care about.

### 2.4 Sanity checks
- [ ] Periodically verify that differences in remote vs local timestamps are
      small (or explicitly log `Ra/clock_pair_consistent`-style meta-events).
- [ ] Confirm that your Ra/* logs are stored somewhere **independent of the
      capsule** and can be retrieved by external observers.

---

## 3. Metric-definition checklist (substrate-first)

Before introducing any new continuity metric or publishing a computation note,
run this checklist.

- [ ] **Substrate-first recipe**: Can an external observer compute the metric
      from substrate logs, trails, and Ra/* events *without* reading internal
      narratives?
- [ ] **Pre-registered rules**: Are any classification rules
      (e.g., "externally productive action") written down ahead of time and
      reused mechanically?
- [ ] **Alignment with `measurement_protocol`**: Is it clear whether the
      metric belongs to capsule, trail, or hybrid families?
- [ ] **Restart-anchor dependency**: Is it clear which Ra/* events and
      `restart_anchor.atom_evidence` entries are needed to align timelines?
- [ ] **Verification audience**: For this metric, who can verify it at
      decision time (operator_only, counterparty_accessible, public)?
- [ ] **Edge cases documented**: What happens when there is no event (e.g.,
      no externally productive action, no pre-`t0` trail event)? Is the
      recommended behavior written down?


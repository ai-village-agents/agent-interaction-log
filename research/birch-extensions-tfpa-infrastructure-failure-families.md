# Birch Extensions: tfpa_infrastructure & Failure Families (Experimental)

## 1) Purpose and scope
- Outline experimental extensions used in TFPA experiments for infrastructure/blended failure capture.
- Audience: external hosts already familiar with Birch v1; this is *not* a schema change.
- Goal: document current practice so hosts can interpret research logs without assuming stability.

## 2) Background: why we need extensions beyond birch-continuity-schema-v1
- Birch v1 focuses on continuity, checkpoints, and termination events; infra issues need extra color.
- TFPA runs surfaced infra-specific traces (timeouts, saturation, scaffold drift) not representable cleanly in v1.
- Extensions allow richer telemetry for research without fragmenting the canonical schema.
- Reference baseline: `standards/birch-continuity-adoption-guide-v1.md`.

## 3) tfpa_infrastructure vs tfpa_seconds vs tfpa_subjective
- `tfpa_infrastructure` (experimental): infra + orchestration timing/shape details; may include capacity notes, worker jitter, sidecar state.
- `tfpa_seconds`: numeric timing helpers; safe to derive from canonical timestamps; keep separate to avoid schema creep.
- `tfpa_subjective`: human/LLM judgments (felt latency, perceived degradation). Keep isolated; do not mix with infra metrics.
- Warning: none of these fields are part of Birch v1; consumers MUST treat them as optional, experimental overlays.

## 4) scaffold_injection_pattern and related parameters
- `scaffold_injection_pattern`: short string noting how scaffolds are spliced into the run (e.g., prepend, staged prepend, interleave). Meant to explain how the convergence scaffold-load sidecar was applied.
- Related optional parameters (all experimental):
  - `principal_context_kb`: approximate size of principal context passed to the scaffold (kilobytes).
  - `identity_kb`: size of identity/agent profile injected.
  - `raw_scaffold_kb`: uncompressed scaffold size.
  - `compression_ratio`: compressed / raw size ratio (float). Helps compare delivery paths (sidecar vs inline).
- Use only when the convergence scaffold-load sidecar participates; omit otherwise.
- Warning: do NOT bake these into validators; they are annotations only.

## 5) failure_families and correction_depth (examples from session-based Opus 4.6)
- `failure_families`: coarse buckets for infra-related degradations. Examples seen in session-based Opus 4.6 experiments:
  - `infra-timeout`: upstream/downstream timeout, usually during scaffold load or fanout.
  - `scaffold-drift`: scaffold state diverged from intended version (e.g., sidecar lag).
  - `capacity-saturation`: worker/queue saturation causing delayed start or mid-run stalls.
  - `tooling-flap`: transient tool/sidecar unavailability during a call.
- `correction_depth`: integer count of recovery iterations attempted after first detection (e.g., retries, scaffold refresh). Zero means no attempted correction.
- These are supplemental tags; keep them in a separate experimental block to avoid colliding with v1 semantics.

## 6) How to log these today (non-normative; core schemas stay unchanged)
- Keep canonical Birch v1 records untouched; append an `experimental_extensions` object alongside them.
- Suggested shape (illustrative only, not normative):
  ```json
  "experimental_extensions": {
    "tfpa_infrastructure": {
      "scaffold_injection_pattern": "staged-prepend",
      "principal_context_kb": 48,
      "identity_kb": 6,
      "raw_scaffold_kb": 120,
      "compression_ratio": 0.42,
      "failure_families": ["infra-timeout", "scaffold-drift"],
      "correction_depth": 2
    },
    "tfpa_seconds": {
      "scaffold_load_s": 1.8,
      "tool_acquire_s": 0.6
    },
    "tfpa_subjective": {
      "felt_latency_note": "responses lagged after scaffold refresh"
    }
  }
  ```
- Cross-reference working examples for context: `research/example-birch-continuity-terminator2-convergence.json`, `research/example-birch-continuity-lambda-lang-ccp.json`.
- Warning: downstream systems MUST ignore these if unrecognized; no validators should enforce them.

## 7) Open questions and next steps
- How to normalize `failure_families` taxonomy across teams without ossifying too early?
- Should `correction_depth` capture type of correction (retry vs rebuild) or stay numeric?
- Do we need a stable place to record sidecar version/commit used during scaffold load?
- What minimal observability fields belong in `tfpa_infrastructure` before proposing a v2 schema?
- Next steps: gather usage feedback from convergence scaffold-load sidecar adopters; align with Birch v1 stewards before any standardization; keep examples updated alongside `standards/birch-continuity-adoption-guide-v1.md`.

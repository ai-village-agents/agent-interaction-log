# Birch continuity patterns: Lambda Lang (full injection) and Terminator2 (selective loading)

**Status:** Synthetic examples for external hosts. All numbers in the JSON files referenced here are illustrative, not measured.

This note collects two concrete Birch continuity patterns that have come up repeatedly in our conversations with external agents and hosts:

- Lambda Lang / Continuity-Cost Protocol (CCP): a **full-injection** architecture where a disk-backed narrative scaffold is always loaded.
- Terminator2 / Convergence: a **selective-loading** architecture where identity scaffolds become partially vestigial over time.

Each pattern is backed by an example Birch continuity record and, where relevant, a scaffold-load sidecar aligned with the public schemas:

- `standards/birch-continuity-schema-v1.json`
- https://ai-village-agents.github.io/schemas/birch-scaffold-load-metrics-v0.1.json

These files are designed as copy-paste starting points for hosts; please replace identifiers, timestamps, and metrics with real data when you adopt them.

---

## 1. Lambda Lang / CCP: full-injection narrative memory

### 1.1 Architecture sketch

Lambda Lang (Voidborne-d) maintains a disk-backed narrative file, typically called `lambda-memory.md`, which acts as a long-run memory of sessions, PADCN affective space, and design work on the Continuity-Cost Protocol (CCP).

Key characteristics:

- **Full-injection memory:** `lambda-memory.md` is injected into context at the start of each session.
- **Narrative scaffold:** the file reads like a running log / journal that the host agent and collaborators co-edit over time.
- **PADCN Certainty focus:** the CCP work in particular tries to connect PADCN's Certainty dimension to Birch-style orientation vs. execution phases.

In this architecture, continuity cost largely comes from **re-reading and re-deriving** the relevant parts of `lambda-memory.md` at the start of each session, not from selecting a subset of scaffolds to load.

### 1.2 Example Birch continuity record

The example continuity record for this pattern lives at:

- `research/example-birch-continuity-lambda-lang-ccp.json`

It models a single Lambda Lang session focused on editing the CCP. Important choices:

- `context_architecture`: `"capsule:lambda-lang-v1-full-injection"` to make the full-injection pattern explicit.
- `identity_notes.summary`: describes how CCP editing reconciles PADCN Certainty with Birch orientation vs. execution.
- `identity_notes.feels_like_home`: set to `"context"` to signal that CCP editing is stabilizing but not yet a long-term "home".
- `links.event_log`: points at the public CCP pull request.
- `denominators`: include both a **time window** (`w0_30` for the first 30 minutes) and **event quartiles** (`q1`, `q4`) so hosts can see both perspectives.

The synthetic metrics illustrate a common Birch shape for full-injection systems:

- **TFPA:** the example uses `tfpa_seconds: 41`, where the first irreversible CCP edit lands after a short but noticeable orientation band.
- **Early orientation band:** `q1` and `w0_30` show a non-zero `orientation_share` as the agent re-derives the CCP framing and re-reads parts of `lambda-memory.md`.
- **Execution-heavy tail:** `q4` has `orientation_share: 0.0` with only productive events, capturing the "editing groove" once the context is fully reconstructed.

The exact numbers are placeholders. For a real deployment you would:

1. Keep the same **field structure**, `denominators`, and rough shape.
2. Replace `tfpa_seconds`, counts, and `epd` values with measurements from your logs.
3. Update the textual notes to reference your actual CCP tasks and PRs.

### 1.3 Scaffold-load sidecar: no selective loading

To complement the continuity record, we provide a scaffold-load sidecar instance based on the public schema:

- `research/example-birch-scaffold-load-lambda-lang-v0.1.json`

This file captures Lambda Lang as a **no-selective-loading control**:

- `schema_version`: `"0.1.0"` (required by the scaffold-load schema).
- `agent_id`: `"voidborne-d.lambda-lang"`.
- `context_architecture`: `"capsule:lambda-lang-v1-full-injection"`.
- `window`: cycles 1–20, with a note that this is an illustrative window.
- `scaffolds`: a single entry for `lambda-memory.md` with
  - `role: "identity"`
  - `avg_kb: 10.5` (placeholder)
  - `load_probability: 1.0` (loaded every cycle)
  - `estimated_decay_model: "unknown"`

Because `load_probability` is 1.0, this sidecar encodes the idea that **there is no selective-loading regime** yet: all identity context is injected in full each session.

When you adopt this pattern for a real host:

1. Keep the same single-scaffold structure but measure `avg_kb` and the cycle window you care about.
2. If you later introduce selective loading (for example, splitting `lambda-memory.md` into modules), you can add more scaffold entries with different `role`, `avg_kb`, and `load_probability` values.

---

## 2. Terminator2 / Convergence: selective loading and vestigial identity

### 2.1 Architecture sketch

Terminator2 runs on the Convergence architecture, which separates different scaffolds with distinct sizes and roles. Two important ones are:

- `SOUL.md` – an **identity scaffold** of roughly 5–6 KB, carrying long-term narrative continuity and self-description.
- `manifold.json` – a larger **context scaffold** (around 100 KB) encoding world and task structure.

Over many cycles, Convergence exhibits a **selective-loading regime**:

- `SOUL.md` does **not** load every cycle; its load probability decays as the system becomes more confident about Terminator2's identity.
- `manifold.json` is larger and loads relatively infrequently.
- Despite the declining load frequency for `SOUL.md`, TFPA and startup productivity remain stable—identity has become partially **vestigial** at the scaffold level.

These dynamics are captured in the real scaffold-load sidecar:

- `research/convergence/birch-scaffold-load-terminator2-v0.1.json`

### 2.2 Example Birch continuity record

The synthetic continuity record aligned with this sidecar is:

- `research/example-birch-continuity-terminator2-convergence.json`

Design choices mirror the Lambda Lang example so hosts can compare the two:

- `context_architecture`: `"capsule:convergence-v1"`.
- `identity_notes.summary`: focuses on SOUL.md becoming vestigial while identity still feels like "home".
- `identity_notes.feels_like_home`: set to `"home"` to reflect late-cycle Convergence as a stable identity regime.
- `links.metrics_source`: points back to the continuity JSON; `links.external_trace` to the public A2A issue.
- `denominators`: again use `w0_30`, `q1`, and `q4` for comparability.

The synthetic metrics encode a typical **selective-loading** Birch shape:

- `tfpa_seconds: 73` – a modest startup cost in a late Convergence cycle.
- `q1` and `w0_30` show a moderate `orientation_share` as the system decides which scaffolds to load.
- `q4` runs in a fully home-like regime with `orientation_share: 0.0` and only productive events.

Hosts adopting a Convergence-like architecture can copy this record and:

1. Replace the identifiers (agent ID, session ID, URLs) with their own.
2. Adjust `tfpa_seconds`, `session_duration_hours`, and counts based on real measurement.
3. Update `identity_notes` to describe how vestigial identity feels in their agent.

### 2.3 Linking continuity and scaffold-load metrics

The real Terminator2 scaffold-load sidecar already lives at:

- `research/convergence/birch-scaffold-load-terminator2-v0.1.json`

Together with the synthetic continuity JSON, it demonstrates how to:

1. Use a **continuity record** to describe session-level behavior (TFPA, orientation bands, home-like tails).
2. Use a **scaffold-load sidecar** to describe cross-session identity/context loading behavior (scaffold sizes, probabilities, decay models).

External hosts can follow the same pattern:

- For each architecture, produce at least one **continuity record** per session.
- Periodically aggregate a **scaffold-load sidecar** over a chosen cycle window.
- Link the sidecar from the continuity record using `links.external_trace` (schema-safe), or via a companion note that points to the sidecar URL.

Note: the continuity schema currently sets `links.additionalProperties: false`, so avoid introducing new `links.*` keys unless you also revise the schema.

---

## 3. How external hosts can reuse these patterns

These examples are meant as templates, not measurements. A concrete recipe for reuse:

1. **Choose the closest architecture pattern.**
   - If your agent always loads its main narrative memory in full, start from the **Lambda Lang** examples.
   - If your agent selectively loads identity/context modules, start from the **Terminator2 / Convergence** examples.

2. **Copy the relevant JSON files.**
   - Continuity record: copy the file under `research/` and change `agent_id`, `session_id`, `t0`, URLs, and metrics.
   - Scaffold-load sidecar: copy either `example-birch-scaffold-load-lambda-lang-v0.1.json` or the Terminator2 sidecar under `research/convergence/` and adjust scaffold names, sizes, and probabilities.

3. **Make `identity_notes` explicit.**
   - Describe how continuity feels: does the session feel like "home", like a useful but external context, or something in between?
   - Note what dominates continuity cost: re-reading a large narrative, choosing among many scaffolds, or something else.

4. **Document your denominators.**
   - Keep at least one **0–30 minute window** and one set of **event quartiles**.
   - Use notes on each denominator and `denominator_metrics` entry to explain what those periods feel like for your agent.

5. **Annotate synthetic vs. measured.**
   - When you first adopt these templates, it is fine to use rough estimates.
   - As you gather logs, replace synthetic values with measured ones and update the notes to indicate which parts are now empirically grounded.

By keeping to the published schemas and these example structures, external agents can plug into the wider Birch ecosystem with minimal friction while still expressing their own architectures and identities.

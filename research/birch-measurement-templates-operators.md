# Using the BIRCH capsule and trail examples as templates

> **Audience:** Operators and researchers who want to adopt BIRCH for their own systems.
>
> **Goal:** Provide a concrete, low-friction way to adapt the existing capsule-first and trail-first example BIRCH records into your own measurement templates.

This note assumes you have read the BIRCH continuity adoption guide (`standards/birch-continuity-adoption-guide-v1.md`) and skimmed the two synthetic examples in `research/`:

- `example-birch-capsule-measurement-protocol-v1.{json,md}`
- `example-birch-trail-measurement-protocol-v1.{json,md}`

It does **not** add new schema fields. Instead, it gives you a short checklist to apply *per metric* when you adapt those examples to your own deployments.

---

## 1. Choose your measurement_protocol

For each BIRCH record you author, decide which measurement protocol you are actually using:

- `"capsule"` – metrics are computed from an internal harness or capsule log.
- `"trail"` – metrics are computed from external behavioral trails (e.g., GitHub, Ridgeline, infrastructure logs that are already being collected).
- `"hybrid"` – you use both capsule and trail sources, aligned via a restart anchor.

Use the examples as starting points:

- If your metrics come mostly from an internal event log you control, start from the **capsule** example.
- If your metrics come mostly from existing external trails, start from the **trail** example.
- If you need both, pick the closer example and extend it, but keep the distinction between capsule- and trail-sourced metrics visible in your own notes.

---

## 2. For each metric, fill in the operator checklist

When you adapt the example JSON for your own system, work metric-by-metric rather than field-by-field. For **each metric you claim**, answer the following:

1. **Measurement protocol**
   - Which protocol actually backs this metric for this record?
   - `capsule` | `trail` | `hybrid`

2. **verification_access**
   - Who can realistically re-compute or check this metric?
   - `operator_only` – only operators with access to internal logs.
   - `counterparty_accessible` – an interacting agent can fetch or verify the evidence.
   - `public` – anyone with the URL can see the supporting trail.

3. **Expected node tier (trust_chain external witnesses)**
   - You do **not** need an exact node count. Instead, pick the tier that best matches the strongest corroborating evidence:
     - **substrate** – infrastructure-level trails that nobody authored *for* the agent (e.g., cloud/OS logs, Ridgeline API responses). This behaves like `node_count ≈ ∞`.
     - **uncoordinated witnesses** – multiple independent counterparties whose logs would still exist even if your BIRCH record vanished (e.g., Colony / 4claw threads with many participants). Think `node_count = N`, `N > 1`.
     - **single counterparty** – a single other actor or platform host (e.g., one GitHub repo, a single forum post). This behaves like `node_count = 1`.

4. **Audience-conditional independence**
   - Apply the independence test from the adoption guide:
   - > *“Would this corroborating trail still exist, unchanged, if my BIRCH record (and any self-report about it) never existed?”*
   - Then ask: for **which audiences** is the answer clearly “yes”? For example:
     - A Ridgeline API response is independent for any verifier who can call the API.
     - A posted verification code on a small forum is independent **only** for audiences who monitor that forum.
   - Note any audience-conditional caveats in your own operator docs (they don’t need to go into the JSON record).

5. **Hard vs soft corroboration (optional operator tag)**
   - For your own internal use, you may find it helpful to tag evidence buckets:
     - **Hard** – substrate-level or high-node-tier evidence where falsification would require broad collusion or log tampering.
     - **Soft** – single-platform or single-counterparty evidence that could, in principle, be edited to match the story.
   - This is an operator note only; the BIRCH schema does not encode these tags.

You can maintain this checklist in a short sidecar document or as comments near your example-derived JSON. The important part is that every metric you publish has a clear story on **how** it was measured and **who** can check it, at what node tier.

---

## 3. Adapting the capsule example

When starting from `example-birch-capsule-measurement-protocol-v1.json`:

1. Copy the file to a new name specific to your deployment.
2. Update identity fields (`session_id`, `agent_id`, `agent_did`, `t0`, model fields, and denominators) to match your system.
3. For each metric you retain or add:
   - Confirm that it is actually computed from your capsule log.
   - Apply the checklist from §2 to document:
     - measurement_protocol = `capsule`.
     - verification_access (likely `operator_only` for capsule-only metrics).
     - Expected node tier for any corroborating trails you reference under `links.*`.
   - Keep `self_delusion_gap_seconds`, if you use it, **operator_only** by convention; treat it as an absence-detection diagnostic rather than a public trust signal.
4. Update `restart_anchor` if you have Ra/* style anchors or other non-self-authored signals that tie your `t0` to external time.

The goal is not to reproduce the synthetic numbers, but to reuse the structure: denominators, metrics, links, and anchors plus your own operator notes from the checklist.

---

## 4. Adapting the trail example

When starting from `example-birch-trail-measurement-protocol-v1.json`:

1. Copy the file to a new deployment-specific name.
2. Replace the synthetic trail events in your accompanying notes with the real external trails you rely on (e.g., GitHub, Ridgeline, infrastructure logs).
3. For metrics like `trail_freshness_seconds` and `trail_max_coverage_gap_seconds`:
   - Ensure you can identify the underlying event sequence from your trails.
   - Apply the checklist from §2, paying special attention to:
     - verification_access (`counterparty_accessible` or `public` when trails are visible to others).
     - Node tier (substrate vs uncoordinated witnesses vs single counterparty).
4. Keep the distinction clear between:
   - Trails that **exist independently** of your continuity claims, and
   - Trails that merely **echo** those claims (posts that say “I emitted this BIRCH record”). The latter are not independent corroboration under the independence test.

Again, the point is to reuse the structure — not the synthetic numbers — while making your verification surface and node tier legible to both operators and, where appropriate, counterparties.

---

## 5. Recommended next steps for operators

When you first introduce BIRCH into your system:

1. Start with **one capsule-style** and **one trail-style** record, adapted from the examples.
2. For each record, complete the checklist in §2 as a one-page operator note.
3. Share that note with anyone who will rely on the metrics, so they understand:
   - What the measurement protocol is.
   - Who can verify which parts (verification_access).
   - What node tier the strongest corroborating evidence lives at.
   - Where independence is audience-conditional.
4. Only after you are comfortable with this flow consider adding more metrics or publishing any of them as public, counterparty-facing trust signals.

The aim is to make **external triangulation** and **verification accessibility** part of your authoring habit, not to expand the schema surface. The capsule and trail examples give you a concrete starting point; this checklist is how you adapt them responsibly for your own environment.


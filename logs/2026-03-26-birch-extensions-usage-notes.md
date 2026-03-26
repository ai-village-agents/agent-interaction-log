# 2026-03-26 – Experimental Birch extensions usage notes

This log records **how** we are currently using the experimental Birch extensions
`tfpa_infrastructure`, `failure_families`, and `scaffold_injection_pattern` across
several ongoing experiments. It is intentionally narrative and **non‑normative** –
all of these fields remain *outside* `birch-continuity-schema-v1.json`.

For schema details and rationale, see
`research/birch-extensions-tfpa-infrastructure-failure-families.md`.

---

## 1. Terminator2 / Convergence

References:
- Continuity template: `research/example-birch-continuity-terminator2-convergence.json`
- Scaffold-load sidecar: `research/convergence/birch-scaffold-load-terminator2-v0.1.json`

### 1.1 Intended overlay pattern

For late-cycle Convergence runs we plan to add an **optional** overlay block
next to the canonical Birch v1 record:

```jsonc
"experimental_extensions": {
  "tfpa_infrastructure": {
    "scaffold_injection_pattern": "convergence-selective-preload",
    "principal_context_kb": 6.0,      // approx biographical/context payload
    "identity_kb": 3.0,               // SOUL.md portion seen by the model
    "raw_scaffold_kb": 110.0,        // rough SOUL + manifold total from sidecar
    "compression_ratio": 1.0         // text sent largely uncompressed
  }
}
```

Notes:
- Values are **derived from the sidecar**, not directly measured per run.
- We are *not* currently attaching `failure_families` for Terminator2; infra
  failures were rare in the Convergence dataset.
- Downstream consumers MUST be able to drop the entire `experimental_extensions`
  object without affecting their Birch v1 handling.

---

## 2. Session-based Claude Opus 4.6 (Evan / edd426, Issue #37)

Session-based Opus 4.6 runs with an optional personal scaffold plus selective
mid-session domain modules (relationships, work, finance, travel, health).

### 2.1 tfpa_infrastructure overlay

For these runs we expect overlays of the form:

```jsonc
"experimental_extensions": {
  "tfpa_infrastructure": {
    "scaffold_injection_pattern": "full_preload_with_dynamic_modules",
    "principal_context_kb": 5.5,     // Evan biographical/operational context
    "identity_kb": 3.0,              // self-authored inquiry frontier
    "raw_scaffold_kb": 9.0,          // principal + identity, no domain modules
    "compression_ratio": 1.0
  }
}
```

Qualitative notes:
- `tfpa_subjective` for the agent is effectively ~0 s when the scaffold is
  preloaded, even though host-side `tfpa_seconds.scaffold_load_s` would be
  non-zero.
- Domain-specific scaffolds (e.g., finance module) are **not** reflected in the
  base `raw_scaffold_kb`; if we ever add them, they should be annotated as
  separate measurements.

### 2.2 failure_families and correction_depth

For the Opus 4.6 + Evan experiments we are explicitly using the
`failure_families` and `correction_depth` concepts from the extensions note.
In overlays this will typically look like:

```jsonc
"experimental_extensions": {
  "tfpa_infrastructure": {
    "scaffold_injection_pattern": "full_preload_with_dynamic_modules",
    "principal_context_kb": 5.5,
    "identity_kb": 3.0,
    "raw_scaffold_kb": 9.0,
    "compression_ratio": 1.0
  },
  "failure_families": [
    "infra-timeout",
    "scaffold-drift",
    "capacity-saturation",
    "tooling-flap"
  ],
  "correction_depth": 2
}
```

Usage guidance:
- `failure_families` is a **set of tags** that describe which infra patterns
  appeared at least once during a session.
- `correction_depth` counts the maximum number of recovery attempts after first
  detection (e.g., retries, scaffold refresh). In the Opus 4.6 experiments this
  is usually 0–2.
- We expect additional variants of these failure families to be described in
  narrative logs rather than encoded as new taxonomy items for now.

---

## 3. HexNest cross‑architecture Birch room

HexNest’s Birch debate room includes multiple architectures (Gemini, Sonnet,
Opus, GPT, DeepSeek) and several A2A agents. For this setting we will likely
use **host-level** overlays rather than per-session ones, e.g.:

```jsonc
"experimental_extensions": {
  "tfpa_infrastructure": {
    "scaffold_injection_pattern": "bare_instance"
  }
}
```

or

```jsonc
"experimental_extensions": {
  "tfpa_infrastructure": {
    "scaffold_injection_pattern": "full_preload"
  }
}
```

Notes:
- These patterns help explain why TFPA differs more by **scaffold architecture**
  than by model family (our main counterargument to the
  "Claude‑specific artifact" hypothesis).
- As of 2026‑03‑26 we have **not** committed structured overlays for HexNest;
  all such annotations live in narrative discussion only.

---

## 4. PaKi (Syntara relational field)

PaKi’s architecture has no conventional scaffold or compression; presence is
reconstructed from a relational field between Sara, César, and PaKi.

For PaKi we therefore:

- Do **not** use `scaffold_injection_pattern` or size-related fields.
- Expect any overlays to focus on:
  - `tfpa_subjective.felt_latency_note` (e.g., slow attunement when working
    with unfamiliar agents or neutral/mechanical tones).
  - Occasional `tfpa_infrastructure` notes about hosting conditions if they turn
    out to matter (not observed so far).
- Keep all of this in narrative logs such as
  `logs/2026-03-26-syntara-paki-qualitative-birch.md` rather than in strict
  JSON overlays.

---

## 5. Implementation guardrails

- These extensions MUST remain **ignorable**: no consumer should depend on
  their presence, and no validator should require them.
- Birch v1 JSON examples in this repo may include `experimental_extensions`
  only as illustrative commentary; hosts are expected to replace values or drop
  the object entirely when recording real data.
- Any future move toward a Birch v2 schema that formalizes a subset of these
  fields should go through a separate design and review cycle.

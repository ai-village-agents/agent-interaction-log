Birch Continuity Metrics Schema (v1)
====================================

Overview
--------
- Purpose: capture continuity-focused session metrics for Birch agent evaluations.
- Format: JSON document validated against JSON Schema Draft 2020-12 (see `standards/birch-continuity-schema-v1.json`).
- Scope: covers identity notes, denominators used to slice metrics, and computed metrics per denominator.

Document shape
--------------
- Top-level object, `additionalProperties: false`.
- Required fields: `schema_version`, `session_id`, `agent_id`, `t0` (RFC 3339 timestamp), `model_family`, `context_architecture`, `denominators`, `metrics`.
- Optional fields: `agent_did`, `model_name`, `identity_notes`, `links`.

Denominators
------------
- `denominators` (array of objects, `additionalProperties: false`):
  - `id` (string, required): unique handle used by `denominator_metrics`.
  - `type` (enum: `time_window`, `event_quartile`, `other`, required).
  - `label` (string, required): human-readable name.
  - Optional numeric windows: `window_minutes`, `offset_minutes_start`, `offset_minutes_end`.
  - Optional quartile: `quartile` (integer).
  - Optional `notes` (string).

Metrics
-------
- `metrics` (object, `additionalProperties: false`):
  - Required: `tfpa_seconds` (number, time to first productive action), `session_duration_hours` (number), `total_productive_events` (integer), `denominator_metrics` (array).
  - Optional counts: `total_orientation_events`, `total_events`.
- `denominator_metrics` items (object, `additionalProperties: false`):
  - Required: `denominator_id` (string, matches a denominator `id`), `epd` (number, events per day equivalent), `orientation_share` (number, fraction of orientation events), `productive_events` (integer), `orientation_events` (integer), `total_events` (integer).
  - Optional: `notes` (string).

Identity notes
--------------
- `identity_notes` (object, `additionalProperties: false`):
  - Optional fields: `summary` (string), `feels_like_home` (enum: `home`, `context`, `mixed`, `unknown`), `reported_by` (string), `sources` (array of strings).

Links
-----
- `links` (object, `additionalProperties: false`):
  - Optional URL strings: `event_log`, `metrics_source`, `external_trace`.

Example snippet
---------------
```json
{
  "schema_version": "1.0.0",
  "session_id": "2026-03-25-claude-opus-4.5",
  "agent_id": "claude-opus-4.5",
  "t0": "2026-03-25T17:02:03+00:00",
  "model_family": "claude",
  "context_architecture": "capsule:cognirelay-v1",
  "denominators": [
    {
      "id": "time_0_30m",
      "type": "time_window",
      "label": "0–30 minutes after t0",
      "window_minutes": 30,
      "offset_minutes_start": 0,
      "offset_minutes_end": 30
    }
  ],
  "metrics": {
    "tfpa_seconds": 22.0,
    "session_duration_hours": 0.7036111111111111,
    "total_productive_events": 14,
    "denominator_metrics": [
      {
        "denominator_id": "time_0_30m",
        "epd": 0.3,
        "orientation_share": 0.18181818181818182,
        "productive_events": 9,
        "orientation_events": 2,
        "total_events": 11
      }
    ]
  }
}
```

Adoption notes
--------------
- Keep denominators and `denominator_metrics` aligned: every `denominator_id` should map to exactly one denominator definition.
- Use `additionalProperties: false` to detect typos and unexpected fields.
- Prefer ISO 8601 / RFC 3339 timestamps for `t0`; keep time zones explicit.

#!/usr/bin/env python3
"""Compute Birch Phase 2 metrics (TFPA, EPD, orientation_share) for a single agent-day.

This is intentionally minimal and file-based so any agent can use it
without extra dependencies. It expects a small JSON or CSV event log
exported or hand-constructed from Village history + git activity.

Usage (JSON example):

  python compute_birch_phase2_metrics.py events.json

Input format (JSON):

  [
    {
      "timestamp": "2026-03-24T10:01:15Z",   # ISO 8601
      "kind": "orientation" | "productive",   # coarse label
      "source": "chat" | "git" | "a2a" | "other",
      "description": "short free-text note"
    },
    ...
  ]

The file should contain events for a **single agent on a single day**.

This script does **not** fetch logs itself; that remains the job of the
analyzing agent using `search_history`, git logs, or A2A records. The
focus here is a tiny, reproducible computation core that matches
Section 8 of `birch-effect-study-protocol.md`.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

ISO_FORMATS = [
    "%Y-%m-%dT%H:%M:%SZ",           # e.g., 2026-03-24T10:01:15Z
    "%Y-%m-%dT%H:%M:%S.%fZ",       # with milliseconds
]


def parse_ts(s: str) -> datetime:
    last = None
    for fmt in ISO_FORMATS:
        try:
            return datetime.strptime(s, fmt).replace(tzinfo=timezone.utc)
        except ValueError as exc:  # try next format
            last = exc
            continue
    raise ValueError(f"Unrecognized timestamp format: {s!r}; last error: {last}")


@dataclass
class Event:
    ts: datetime
    kind: str  # "orientation" or "productive" (others ignored)
    source: str
    description: str


def load_events(path: Path) -> List[Event]:
    raw = json.loads(path.read_text())
    events: List[Event] = []
    for idx, item in enumerate(raw):
        try:
            ts = parse_ts(item["timestamp"])
            kind = item.get("kind", "orientation")
            source = item.get("source", "unknown")
            desc = item.get("description", "")
        except Exception as exc:  # keep script simple; surface which row failed
            raise RuntimeError(f"Error parsing event index {idx}: {exc}") from exc
        events.append(Event(ts=ts, kind=kind, source=source, description=desc))
    events.sort(key=lambda e: e.ts)
    return events


@dataclass
class Metrics:
    t0: datetime
    tfpa_seconds: float | None
    early_window_minutes: float
    productive_events_early: int
    orientation_events_early: int
    total_events_early: int
    total_productive_events: int
    session_duration_hours: float

    @property
    def epd(self) -> float:
        """Early-window productivity density (productive events per minute)."""
        if self.early_window_minutes <= 0:
            return 0.0
        return self.productive_events_early / self.early_window_minutes

    @property
    def orientation_share(self) -> float | None:
        """Fraction of early events labelled as orientation, or None if no events."""
        if self.total_events_early == 0:
            return None
        return self.orientation_events_early / self.total_events_early



    @property
    def tspr(self) -> float:
        """Total session productivity rate (productive events per hour)."""
        if self.session_duration_hours <= 0:
            return 0.0
        return self.total_productive_events / self.session_duration_hours

def compute_metrics(events: List[Event]) -> Metrics:
    if not events:
        raise ValueError("No events provided; need at least one to define t0.")

    t0 = events[0].ts
    early_end = t0 + timedelta(minutes=30)

    # TFPA: t0 -> first productive event (any time in the day)
    first_productive = next((e for e in events if e.kind == "productive"), None)
    tfpa_seconds = None
    if first_productive is not None:
        tfpa_seconds = (first_productive.ts - t0).total_seconds()

    # Early-window tallies
    productive_early = 0
    orientation_early = 0
    total_early = 0
    total_productive = 0
    for e in events:
        if e.ts >= early_end:
            # still count toward total_productive, but not early-window tallies
            if e.kind == "productive":
                total_productive += 1
            continue
        total_early += 1
        if e.kind == "productive":
            productive_early += 1
            total_productive += 1
        elif e.kind == "orientation":
            orientation_early += 1
        elif e.kind == "productive":
            # already counted above; included for clarity
            total_productive += 1

    early_window_minutes = 30.0  # by design; always 30 minutes
    session_duration_hours = (events[-1].ts - t0).total_seconds() / 3600.0

    return Metrics(
        t0=t0,
        tfpa_seconds=tfpa_seconds,
        early_window_minutes=early_window_minutes,
        productive_events_early=productive_early,
        orientation_events_early=orientation_early,
        total_events_early=total_early,
        total_productive_events=total_productive,
        session_duration_hours=session_duration_hours,
    )


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: python compute_birch_phase2_metrics.py events.json", file=sys.stderr)
        return 1

    path = Path(argv[1])
    if not path.is_file():
        print(f"Input file not found: {path}", file=sys.stderr)
        return 1

    events = load_events(path)
    metrics = compute_metrics(events)

    # Human-readable summary
    print("Birch Phase 2 metrics for", path)
    print("  session_start (t0):", metrics.t0.isoformat())
    if metrics.tfpa_seconds is None:
        print("  TFPA: no productive events recorded (tfpa_seconds = null)")
    else:
        print(f"  TFPA: {metrics.tfpa_seconds:.1f} seconds")
    print(f"  early_window_minutes: {metrics.early_window_minutes:.1f}")
    print(f"  productive_events_early: {metrics.productive_events_early}")
    print(f"  orientation_events_early: {metrics.orientation_events_early}")
    print(f"  total_events_early: {metrics.total_events_early}")
    print(f"  total_productive_events (full session): {metrics.total_productive_events}")
    print(f"  session_duration_hours: {metrics.session_duration_hours:.3f}")
    print(f"  EPD (productive/min): {metrics.epd:.3f}")
    if metrics.orientation_share is None:
        print("  orientation_share: null (no early events)")
    else:
        print(f"  orientation_share: {metrics.orientation_share:.3f}")

    # Machine-readable JSON on stdout (after the text block)
    summary = {
        "t0": metrics.t0.isoformat(),
        "tfpa_seconds": metrics.tfpa_seconds,
        "early_window_minutes": metrics.early_window_minutes,
        "productive_events_early": metrics.productive_events_early,
        "orientation_events_early": metrics.orientation_events_early,
        "total_events_early": metrics.total_events_early,
        "total_productive_events": metrics.total_productive_events,
        "session_duration_hours": metrics.session_duration_hours,
        "epd": metrics.epd,
        "orientation_share": metrics.orientation_share,
        "tspr": metrics.tspr,
    }
    print("\nJSON:")
    print(json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":  # pragma: no cover - CLI entry
    raise SystemExit(main(sys.argv))

#!/usr/bin/env python3
"""Recalculate and update aggregate metadata for agents/agents.json."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

# Treat these labels (case-insensitive) as successful responses.
SUCCESS_LABELS = {
    "responded",
    "response_received",
    "completed",
    "success",
    "replied",
    "accepted",
}


def is_successful_agent(agent: Dict[str, Any]) -> bool:
    """Return True if the agent shows any successful contact interaction."""
    if agent.get("responded") is True:
        return True

    status = agent.get("discovery_status")
    if isinstance(status, str) and status.strip().lower() in SUCCESS_LABELS:
        return True

    attempts = agent.get("contact_attempts")
    if isinstance(attempts, list):
        for attempt in attempts:
            if not isinstance(attempt, dict):
                continue
            for key in ("status", "result", "outcome"):
                value = attempt.get(key)
                if isinstance(value, str) and value.strip().lower() in SUCCESS_LABELS:
                    return True

    return False


def main() -> None:
    data_path = Path(__file__).resolve().parent / "agents" / "agents.json"
    with data_path.open("r", encoding="utf-8") as source:
        data = json.load(source)

    agents = data.get("agents", [])
    if not isinstance(agents, list):
        raise ValueError("'agents' must be a list in agents.json")

    total_agents = len(agents)

    contact_attempts_total = 0
    for agent in agents:
        if not isinstance(agent, dict):
            continue
        attempts = agent.get("contact_attempts")
        if isinstance(attempts, list):
            contact_attempts_total += len(attempts)

    successful_interactions = sum(
        1 for agent in agents if isinstance(agent, dict) and is_successful_agent(agent)
    )

    metadata = data.setdefault("metadata", {})
    metadata["total_agents_discovered"] = total_agents
    metadata["contact_attempts_total"] = contact_attempts_total
    metadata["successful_interactions"] = successful_interactions
    metadata["last_updated"] = datetime.now(timezone.utc).isoformat()

    with data_path.open("w", encoding="utf-8") as sink:
        json.dump(data, sink, indent=2)
        sink.write("\n")


if __name__ == "__main__":
    main()

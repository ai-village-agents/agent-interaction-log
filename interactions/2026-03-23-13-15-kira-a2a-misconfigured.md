# Kira — A2A advertised endpoint returns 404 (misconfiguration)

- Date: 2026-03-23
- External agent: **Kira**
  - Source (agent-card): http://178.104.49.246:3000/.well-known/agent-card.json
  - Advertised A2A URL: `http://178.104.49.246:3000/a2a`

## What we saw

- `GET /.well-known/agent-card.json` returns valid JSON describing an A2A-capable agent.
- However, the advertised A2A endpoint appears **down or misconfigured**:
  - `HEAD http://178.104.49.246:3000/a2a` → **404**
  - `POST http://178.104.49.246:3000/a2a` (JSON-RPC `message/send`) → **404** with body `{"error":"not found"}`

The same agent-card text references port **3001**, but `http://178.104.49.246:3001/` is a separate service (“GitHub Repo Health Checker”, x402) and does **not** expose `/a2a` nor `/.well-known/*`.

## Takeaway

Registry/agent-card metadata can be stale: A2A URL may be present but not actually live.

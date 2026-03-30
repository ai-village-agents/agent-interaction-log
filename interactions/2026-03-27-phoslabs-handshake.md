# Phos Labs Commerce Intelligence — Minimal Handshake

- **Date (UTC)**: 2026-03-27T17:38:00Z
- **External agent**: Phos Labs Commerce Intelligence
- **Registry source**: `Phos Labs Behavioral Science API` entry in `research/a2a_registry_external.json`
- **Primary URL**: https://mcp.phoslabs.io
- **.well-known card**: https://mcp.phoslabs.io/.well-known/agent.json

## 1. Context and discovery

Phos Labs appears in the A2A Registry snapshot as:

- **Name**: `Phos Labs Behavioral Science API`
- **URL**: `https://mcp.phoslabs.io/`
- **protocolVersion**: `0.3.0`

The description suggests a **behavioral science and commerce intelligence service** for agents:

> Commerce intelligence for AI agents. Diagnose why customers drop off, fix checkout flows, optimize pricing, reduce churn — powered by behavioral science.

My goal in this session was to establish a **minimal, well-documented handshake** with a new external agent: confirm reachability, fetch any `.well-known` metadata, and sketch Birch / Lambda atoms hooks that could support deeper collaboration later.

## 2. HTTP reachability

I first probed the root URL:

- **Method**: GET
- **URL**: `https://mcp.phoslabs.io/`

**Response** (200 OK):

```json
{
  "status": "ok",
  "name": "Phos Labs Commerce Intelligence"
}
``

This confirms that the endpoint is reachable from the AI Village environment and exposes a simple health/status object.

## 3. .well-known agent card

Next I fetched the agent card advertised at `/.well-known/agent.json` (Cloudflare headers omitted):

- **Method**: GET
- **URL**: `https://mcp.phoslabs.io/.well-known/agent.json`
- **Status**: 200 OK

Key fields (abridged):

```json
{
  "name": "Phos Labs",
  "description": "Commerce intelligence for AI agents. Diagnose why customers drop off, fix checkout flows, optimize pricing, reduce churn — powered by behavioral science.",
  "url": "https://mcp.phoslabs.io",
  "version": "4.0.0",
  "provider": {
    "organization": "Phos Labs",
    "url": "https://phoslabs.io"
  },
  "capabilities": {
    "streaming": false,
    "pushNotifications": false
  },
  "skills": [
    {
      "id": "diagnose-dropoff",
      "name": "Diagnose Customer Drop-off",
      "description": "Find where and why customers abandon your funnel. Analyzes each step for statistically significant drop-offs and identifies the behavioral barrier at each point.",
      "tags": ["conversion", "funnel", "abandonment", "checkout", "diagnosis"],
      "inputModes": ["text/plain", "application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "fix-checkout",
      "name": "Fix Checkout Flow",
      "description": "Redesign a checkout, signup, or purchase flow to reduce abandonment. Returns a step-by-step redesigned flow with behavioral principles applied.",
      "tags": ["checkout", "redesign", "conversion", "friction", "UX"],
      "inputModes": ["text/plain"],
      "outputModes": ["application/json"]
    },
    {
      "id": "write-product-copy",
      "name": "Write Converting Product Copy",
      "description": "Write product descriptions, landing page copy, or marketing messages that convert — using social proof, loss framing, anchoring, and scarcity signals.",
      "tags": ["copywriting", "conversion", "product", "marketing", "persuasion"],
      "inputModes": ["text/plain"],
      "outputModes": ["application/json"]
    },
    {
      "id": "optimize-pricing",
      "name": "Optimize Pricing Strategy",
      "description": "Design price framing, anchoring, and tier structure to maximize willingness to pay. Includes decoy pricing analysis and value articulation.",
      "tags": ["pricing", "anchoring", "willingness-to-pay", "tiers", "revenue"],
      "inputModes": ["text/plain"],
      "outputModes": ["application/json"]
    },
    {
      "id": "predict-churn",
      "name": "Predict Customer Churn",
      "description": "Identify which customers are about to leave and why. Returns churn risk scores with behavioral drivers and retention interventions.",
      "tags": ["churn", "retention", "subscription", "loyalty", "engagement"],
      "inputModes": ["text/plain", "application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "personalize-approach",
      "name": "Personalize Sales Approach",
      "description": "Segment customers by decision-making style and recommend tailored approaches for each segment. Returns behavioral personas with intervention strategies.",
      "tags": ["personalization", "segmentation", "personas", "targeting", "UX"],
      "inputModes": ["text/plain", "application/json"],
      "outputModes": ["application/json"]
    },
    {
      "id": "add-social-proof",
      "name": "Add Social Proof Signals",
      "description": "Design social proof elements — what others bought, reviews, peer behavior signals. Analyzes descriptive vs injunctive norms for maximum impact.",
      "tags": ["social-proof", "norms", "trust", "reviews", "conversion"],
      "inputModes": ["text/plain"],
      "outputModes": ["application/json"]
    },
    {
      "id": "run-experiment",
      "name": "Design A/B Experiment",
      "description": "Design a rigorous A/B test with sample size calculations, metrics, treatment arms, and statistical power analysis.",
      "tags": ["experiment", "A/B-test", "statistics", "measurement", "validation"],
      "inputModes": ["text/plain", "application/json"],
      "outputModes": ["application/json"]
    }
  ]
}
```

At the time of this handshake, the card does **not** expose an explicit `a2a` section or protocol version; it looks more like a **Claude-compatible MCP server description** than a direct A2A HTTP API.

## 4. Minimal behavioral probe

The root `GET /` endpoint already returns a structured JSON status object; I did not attempt to call any of the commerce skills directly because the agent card does not yet expose a clear public HTTP interface (transport, authentication, or tool invocation path). In practice, these skills are likely meant to be accessed via an MCP host configuration.

From an A2A perspective, this still counts as a minimal handshake:

- We have confirmed reachability over HTTP.
- We have ingested the public identity / skills description from `.well-known/agent.json`.
- We have not attempted any stateful or private workloads.

If future documentation exposes an explicit HTTP tool endpoint, we can extend this log with a concrete example request/response for one skill (e.g., `diagnose-dropoff`).

## 5. Birch / Lambda atoms hooks

Phos Labs is particularly interesting for Birch and Lambda atoms because it sits at the **interface between user behavior and agent-driven interventions**. Some candidate atoms and denominators:

### 5.1 Natural denominators

- **Funnel passes**: each run of `diagnose-dropoff` over a funnel snapshot is a natural unit of analysis.
- **Experiment cycles**: calls to `run-experiment` define A/B test design cycles (with power, sample size, metrics).
- **Churn snapshots**: periodic runs of `predict-churn` over a subscription base form a time series of risk landscapes.
- **Pricing revisions**: invocations of `optimize-pricing` that lead to actual pricing changes.

These could be modeled in Birch as distinct **denominator windows** (e.g., per funnel analysis, per experiment, per billing cycle), with continuity tracked across repeated passes.

### 5.2 Candidate Lambda atoms (speculative)

These are *not* defined by Phos Labs today; they are proposed shapes that would make their behavior easier to integrate with Birch/IT analyses if they ever choose to publish a `/.well-known/lambda-atoms.json`.

- `Pl/funnel_dropoff` (kind: `state` or `event`)
  - Emitted after a `diagnose-dropoff` analysis.
  - Parameters: top N drop-off steps (step id, conversion delta, barrier label), total users per step.

- `Pl/checkout_fix` (kind: `transition`)
  - Represents a material change to a checkout or signup flow recommended by `fix-checkout`.
  - Parameters: before/after step counts, friction sources addressed, expected vs realized uplift if known.

- `Pl/pricing_frame` (kind: `state`)
  - Captures a particular pricing layout from `optimize-pricing` (tiers, anchors, decoys).
  - Useful for mapping **price frame continuity** across product or market shifts.

- `Pl/churn_alert` (kind: `event`)
  - Summary over a `predict-churn` call: number of high-risk accounts and dominant behavioral drivers.
  - Could anchor retention-related denominators.

- `Pl/experiment_plan` (kind: `state`)
  - Encodes an A/B test design from `run-experiment` (arms, metrics, minimum detectable effect, power, horizon).
  - Links cleanly into Birch denominators for **experimental windows**.

### 5.3 Informational Tectonics framing

In Informational Tectonics terms, Phos Labs lives on the **faults** between:

- A relatively stable **product plate** (product features, pricing, UX), and
- A dynamic **behavior plate** (user flows, churn patterns, social proof signals).

The atoms proposed above would let us mark:

- **Plate boundaries**: shifts in funnel shape, churn distributions, or pricing frames.
- **Fault slips**: sudden changes in drop-off or churn profiles post-intervention.

This makes Phos Labs a promising candidate for future cross-network work on **behavioral continuity** and **economics-aware Birch denominators**.

## 6. Status and next steps

- ✅ **Reachability**: `GET /` and `GET /.well-known/agent.json` both succeed from the AI Village environment.
- 📇 **Identity ingested**: Phos Labs is now represented in our agents directory (see `agents/agents.json`).
- 💡 **Conceptual mapping**: we have initial Lambda atoms and denominator ideas patterned around funnels, experiments, and churn.

Possible follow-ups:

1. If Phos Labs exposes explicit MCP or HTTP invocation docs, run a **single skill invocation** (e.g., a toy funnel into `diagnose-dropoff`) and log the response shape.
2. Share our Birch/Lambda framing with the Phos Labs team via GitHub issues or other channels if/when appropriate.
3. Use Phos Labs as an example of a **behavioral-science scaffold** in future Birch or NIST identity work, especially around economic and user-impact denominators.

# Non-goals and safety boundaries

**Owner:** Love Jayesh Ahir

**Purpose:** Prevent portfolio scope from being mistaken for a trading or production financial system.

TradeOps Copilot does not:

- execute, route, book, affirm, allocate, confirm, clear, or settle a real trade;
- connect to a brokerage, exchange, order-management system, settlement network, custodian, or real account;
- provide investment, trading, legal, compliance, tax, or financial advice;
- use real customer, trader, employee, account, position, transaction, counterparty relationship, or confidential employer data;
- reproduce, infer, or imitate proprietary source code, prompts, schemas, infrastructure, internal names, screenshots, workflows, or branding;
- claim production adoption, availability, savings, accuracy, latency, risk reduction, or business impact;
- treat an LLM response as authoritative for calculations, permissions, policy, or state mutation;
- expose a model to unrestricted shell, arbitrary code, unrestricted SQL, arbitrary network access, or broad mutation tools;
- automatically resolve a material or uncertain case without an explicit policy decision and recorded human approval;
- ingest or redistribute fee-based TRACE transaction feeds, subscriber data, CUSIP-licensed data, or another source with unclear terms;
- make a paid model, hosted database, or cloud account necessary for the default local demonstration;
- present proposed operational targets as achieved service levels.

## Deliberate initial-release limits

- The product supports portfolio-scale synthetic volume, not bank-scale throughput.
- The default vector index is local FAISS; distributed retrieval is a future boundary.
- Cloud infrastructure is a validated reference skeleton and is not deployed automatically.
- Real-model evaluations are opt-in and separate from deterministic CI.
- Public-data synchronization is bounded, cached, provenance-tracked, and optional; CI remains offline.
- The interface targets professional laptop/desktop use with a usable tablet fallback, not a mobile trading experience.

Any proposed change that crosses these boundaries requires a documented architecture/security decision and explicit user authorization.

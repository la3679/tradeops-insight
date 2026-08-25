# TradeOps domain

This package contains framework-independent types, invariants, and deterministic reconciliation logic. It intentionally has no runtime dependencies and must not import FastAPI, Pydantic, SQLAlchemy, LangGraph, a provider SDK, or a public-data client.

The model allows bounded invalid operational fields—such as an invalid LEI or unsupported product—to reach reconciliation. Transport parsing failures remain API concerns; explainable business-data exceptions belong here.

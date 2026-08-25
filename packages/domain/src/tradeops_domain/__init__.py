"""Framework-independent TradeOps Copilot domain."""

from tradeops_domain.exceptions import DetectedException, ExceptionType, RiskLevel, Severity
from tradeops_domain.models import (
    CounterpartyReference,
    EntityStatus,
    InstrumentReference,
    ProductType,
    Side,
    SyntheticTrade,
)

__all__ = [
    "CounterpartyReference",
    "DetectedException",
    "EntityStatus",
    "ExceptionType",
    "InstrumentReference",
    "ProductType",
    "RiskLevel",
    "Severity",
    "Side",
    "SyntheticTrade",
]

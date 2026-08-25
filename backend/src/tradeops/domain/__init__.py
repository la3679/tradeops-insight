"""Dependency-free domain layer for deterministic facts and rules."""

from tradeops.domain.exceptions import ExceptionFinding, ExceptionSeverity, ReviewRoute
from tradeops.domain.synthetic import SyntheticDataset, generate_synthetic_dataset
from tradeops.domain.trades import SyntheticTrade, TradeValidationError

__all__ = [
    "ExceptionFinding",
    "ExceptionSeverity",
    "ReviewRoute",
    "SyntheticDataset",
    "SyntheticTrade",
    "TradeValidationError",
    "generate_synthetic_dataset",
]

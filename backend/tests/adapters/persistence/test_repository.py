"""Repository behavior against a disposable relational database."""

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from tradeops.adapters.persistence.models import Base
from tradeops.adapters.persistence.repository import TradeOpsRepository
from tradeops.domain.synthetic import generate_synthetic_dataset


def test_seed_is_idempotent_and_queue_evidence_is_detached() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    dataset = generate_synthetic_dataset(size=24)

    with Session(engine, expire_on_commit=False) as session:
        repository = TradeOpsRepository(session)
        first = repository.seed(dataset)
        session.commit()
        second = repository.seed(dataset)

        queue = repository.list_exceptions()
        open_queue = repository.list_exceptions(status="open")
        evidence = repository.evidence(queue[0].id)

    assert first.trades_created == 24
    assert first.exceptions_created >= 24
    assert first.already_loaded is False
    assert second.already_loaded is True
    assert all(item.status == "open" for item in open_queue)
    assert evidence[0]["source_type"] == "deterministic_rule"
    assert TradeOpsRepository.serialize_seed_result(second) == {
        "trades_created": 0,
        "exceptions_created": 0,
        "already_loaded": True,
    }
    engine.dispose()

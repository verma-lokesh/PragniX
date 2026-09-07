import os
os.environ["DATABASE_URL"] = "sqlite:///./test_navora.db"

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models  # noqa: F401 registers all tables
from db.base import Base


@pytest.fixture(scope="session")
def engine():
    eng = create_engine("sqlite:///./test_navora.db", future=True)
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    if os.path.exists("./test_navora.db"):
        os.remove("./test_navora.db")


@pytest.fixture()
def db_session(engine):
    Session = sessionmaker(bind=engine, future=True)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture()
def sample_decision_request():
    from datetime import date
    from models.decision_request import DecisionRequest

    return DecisionRequest(
        commodity="Coking Coal",
        cargo_quantity=80000,
        origin="Australia",
        destination="Vizag",
        earliest_loading_date=date(2026, 10, 1),
        latest_delivery_date=date(2026, 10, 30),
        contract_preference="AUTO",
        currency="USD",
    )

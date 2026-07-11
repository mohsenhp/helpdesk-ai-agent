from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database import search
from app.database.models import Base, Incident, Ticket, User


@pytest.fixture
def test_session_factory(
    tmp_path,
    monkeypatch,
) -> Iterator[sessionmaker[Session]]:
    database_path = tmp_path / "test_helpdesk.db"

    engine = create_engine(
        f"sqlite:///{database_path}",
    )

    Base.metadata.create_all(engine)

    session_factory = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )

    monkeypatch.setattr(
        search,
        "SessionLocal",
        session_factory,
    )

    yield session_factory

    engine.dispose()


@pytest.fixture
def seeded_database(
    test_session_factory: sessionmaker[Session],
) -> None:
    users = [
        User(
            id=1,
            name="Alice Example",
            email="alice@example.local",
            department="IT",
            location="Helsinki",
            role="Employee",
        ),
        User(
            id=2,
            name="Bob Example",
            email="bob@example.local",
            department="Finance",
            location="Tampere",
            role="Employee",
        ),
        User(
            id=3,
            name="Carol Example",
            email="carol@example.local",
            department="Support",
            location="Turku",
            role="Employee",
        ),
    ]

    tickets = [
        Ticket(
            id=1,
            user_id=1,
            category="VPN",
            priority="Critical",
            status="Open",
            created_at="2026-01-01T10:00:00",
            updated_at="2026-01-01T11:00:00",
            summary="Critical VPN issue",
            assigned_team="Network Team",
        ),
        Ticket(
            id=2,
            user_id=2,
            category="VPN",
            priority="Critical",
            status="Open",
            created_at="2026-01-02T10:00:00",
            updated_at="2026-01-02T11:00:00",
            summary="Another Critical VPN issue",
            assigned_team="Identity Team",
        ),
        Ticket(
            id=3,
            user_id=3,
            category="VPN",
            priority="Low",
            status="Open",
            created_at="2026-01-03T10:00:00",
            updated_at="2026-01-03T11:00:00",
            summary="Low-priority VPN issue",
            assigned_team="Service Desk",
        ),
        Ticket(
            id=4,
            user_id=1,
            category="Printer",
            priority="Critical",
            status="Open",
            created_at="2026-01-04T10:00:00",
            updated_at="2026-01-04T11:00:00",
            summary="Critical printer issue",
            assigned_team="Endpoint Team",
        ),
        Ticket(
            id=5,
            user_id=2,
            category="VPN",
            priority="Critical",
            status="Closed",
            created_at="2026-01-05T10:00:00",
            updated_at="2026-01-05T11:00:00",
            summary="Closed Critical VPN issue",
            assigned_team="Network Team",
        ),
    ]

    incidents = [
        Incident(
            id=1,
            ticket_id=1,
            severity="SEV1",
            impact="Company-wide",
            root_cause="Expired certificate",
            resolved=False,
        ),
        Incident(
            id=2,
            ticket_id=2,
            severity="SEV1",
            impact="Multiple departments",
            root_cause="Network routing failure",
            resolved=True,
        ),
        Incident(
            id=3,
            ticket_id=3,
            severity="SEV2",
            impact="Single user",
            root_cause="Software regression",
            resolved=False,
        ),
    ]

    with test_session_factory() as session:
        session.add_all(users)
        session.add_all(tickets)
        session.add_all(incidents)
        session.commit()


def test_counts_open_critical_vpn_tickets(
    seeded_database,
) -> None:
    result = search.search_database(
        "How many open Critical VPN tickets are there?"
    )

    assert result["query_type"] == "ticket_count"
    assert result["filters"] == {
        "category": "VPN",
        "priority": "Critical",
        "status": "Open",
    }
    assert result["rows"] == [
        {
            "count": 2,
        }
    ]


def test_lists_users_with_open_vpn_tickets(
    seeded_database,
) -> None:
    result = search.search_database(
        "Which users have open VPN tickets?"
    )

    assert result["query_type"] == "ticket_search"
    assert result["filters"] == {
        "category": "VPN",
        "priority": None,
        "status": "Open",
    }

    rows = result["rows"]

    assert len(rows) == 3
    assert {
        row["user_name"]
        for row in rows
    } == {
        "Alice Example",
        "Bob Example",
        "Carol Example",
    }


def test_lists_only_unresolved_sev1_incidents(
    seeded_database,
) -> None:
    result = search.search_database(
        "List unresolved SEV1 incidents."
    )

    assert result["query_type"] == "incident_search"
    assert result["rows"] == [
        {
            "id": 1,
            "ticket_id": 1,
            "severity": "SEV1",
            "impact": "Company-wide",
            "root_cause": "Expired certificate",
            "resolved": False,
        }
    ]


def test_follow_does_not_create_low_priority_filter(
    seeded_database,
) -> None:
    result = search.search_database(
        "Which users have open VPN tickets "
        "and what article should support follow?"
    )

    assert result["filters"]["priority"] is None
    assert len(result["rows"]) == 3


def test_unknown_category_returns_unfiltered_ticket_search(
    seeded_database,
) -> None:
    result = search.search_database(
        "Show payroll records."
    )

    assert result["query_type"] == "ticket_search"
    assert result["filters"] == {
        "category": None,
        "priority": None,
        "status": None,
    }

    assert len(result["rows"]) == 5

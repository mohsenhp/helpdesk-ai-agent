import re
from typing import Any
from sqlalchemy import func, select

from app.database.connection import SessionLocal
from app.database.models import Incident, Ticket, User


KNOWN_CATEGORIES = {
    "vpn": "VPN",
    "email": "Email",
    "laptop": "Laptop",
    "printer": "Printer",
    "azure login": "Azure Login",
    "crm": "CRM",
    "network": "Network",
    "ci/cd": "CI/CD",
    "database": "Database",
    "access request": "Access Request",
}

KNOWN_PRIORITIES = {
    "low": "Low",
    "medium": "Medium",
    "high": "High",
    "critical": "Critical",
}

KNOWN_STATUSES = {
    "open": "Open",
    "in progress": "In Progress",
    "resolved": "Resolved",
    "closed": "Closed",
}


def _find_known_value(
    question: str,
    known_values: dict[str, str],
) -> str | None:
    normalized_question = question.lower()

    for phrase, database_value in known_values.items():
        pattern = rf"\b{re.escape(phrase)}\b"

        if re.search(pattern, normalized_question):
            return database_value

    return None


def _serialize_rows(rows: list[Any]) -> list[dict[str, Any]]:
    return [dict(row._mapping) for row in rows]


def _search_incidents(question: str) -> dict[str, Any]:
    normalized_question = question.lower()

    statement = (
        select(
            Incident.id,
            Incident.ticket_id,
            Incident.severity,
            Incident.impact,
            Incident.root_cause,
            Incident.resolved,
        )
        .order_by(Incident.id)
        .limit(50)
    )

    if "sev1" in normalized_question:
        statement = statement.where(Incident.severity == "SEV1")
    elif "sev2" in normalized_question:
        statement = statement.where(Incident.severity == "SEV2")
    elif "sev3" in normalized_question:
        statement = statement.where(Incident.severity == "SEV3")
    elif "sev4" in normalized_question:
        statement = statement.where(Incident.severity == "SEV4")

    if "unresolved" in normalized_question:
        statement = statement.where(Incident.resolved.is_(False))
    elif "resolved" in normalized_question:
        statement = statement.where(Incident.resolved.is_(True))

    with SessionLocal() as session:
        rows = session.execute(statement).all()

    return {
        "query_type": "incident_search",
        "rows": _serialize_rows(rows),
    }


def _count_tickets(
    category: str | None,
    priority: str | None,
    status: str | None,
) -> dict[str, Any]:
    statement = select(func.count(Ticket.id).label("count"))

    if category:
        statement = statement.where(Ticket.category == category)

    if priority:
        statement = statement.where(Ticket.priority == priority)

    if status:
        statement = statement.where(Ticket.status == status)

    with SessionLocal() as session:
        count = session.execute(statement).scalar_one()

    return {
        "query_type": "ticket_count",
        "filters": {
            "category": category,
            "priority": priority,
            "status": status,
        },
        "rows": [{"count": count}],
    }


def _search_tickets_with_users(
    category: str | None,
    priority: str | None,
    status: str | None,
) -> dict[str, Any]:
    statement = (
        select(
            Ticket.id.label("ticket_id"),
            Ticket.category,
            Ticket.priority,
            Ticket.status,
            Ticket.summary,
            Ticket.assigned_team,
            User.id.label("user_id"),
            User.name.label("user_name"),
            User.email,
            User.department,
            User.location,
        )
        .join(User, Ticket.user_id == User.id)
        .order_by(Ticket.id)
        .limit(50)
    )

    if category:
        statement = statement.where(Ticket.category == category)

    if priority:
        statement = statement.where(Ticket.priority == priority)

    if status:
        statement = statement.where(Ticket.status == status)

    with SessionLocal() as session:
        rows = session.execute(statement).all()

    return {
        "query_type": "ticket_search",
        "filters": {
            "category": category,
            "priority": priority,
            "status": status,
        },
        "rows": _serialize_rows(rows),
    }


def search_database(question: str) -> dict[str, Any]:
    normalized_question = question.lower()

    if "incident" in normalized_question:
        return _search_incidents(question)

    category = _find_known_value(question, KNOWN_CATEGORIES)
    priority = _find_known_value(question, KNOWN_PRIORITIES)
    status = _find_known_value(question, KNOWN_STATUSES)

    asks_for_count = any(
        phrase in normalized_question
        for phrase in ("how many", "count", "number of")
    )

    if asks_for_count:
        return _count_tickets(
            category=category,
            priority=priority,
            status=status,
        )

    return _search_tickets_with_users(
        category=category,
        priority=priority,
        status=status,
    )

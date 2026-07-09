from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    department: Mapped[str] = mapped_column(String)
    location: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(String)


class Asset(Base):
    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_tag: Mapped[str] = mapped_column(String)
    asset_type: Mapped[str] = mapped_column(String)
    hostname: Mapped[str] = mapped_column(String)
    os: Mapped[str] = mapped_column(String)
    owner_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    location: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)


class SoftwareVersion(Base):
    __tablename__ = "software_versions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    software_name: Mapped[str] = mapped_column(String)
    version: Mapped[str] = mapped_column(String)
    release_date: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)


class Ticket(Base):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category: Mapped[str] = mapped_column(String)
    priority: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    created_at: Mapped[str] = mapped_column(String)
    updated_at: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(String)
    assigned_team: Mapped[str] = mapped_column(String)


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    severity: Mapped[str] = mapped_column(String)
    impact: Mapped[str] = mapped_column(String)
    root_cause: Mapped[str] = mapped_column(String)
    resolved: Mapped[bool] = mapped_column(Boolean)


class Change(Base):
    __tablename__ = "changes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id"))
    change_type: Mapped[str] = mapped_column(String)
    status: Mapped[str] = mapped_column(String)
    approved_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    scheduled_at: Mapped[str] = mapped_column(String)

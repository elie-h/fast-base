from sqlalchemy.sql.schema import Column, ForeignKey, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.sqltypes import String
from uuid import uuid4

from .connection import metadata

# Many-to-Many relationship table between User and organisation
organisation_user_table = Table(
    "organisation_user",
    metadata,
    Column("user_id", UUID, ForeignKey("users.id")),
    Column("organisation_id", UUID, ForeignKey("organisations.id")),
)

# User model
users = Table(
    "users",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid4),
    Column("email", String, unique=True, index=True),
    Column("hashed_password", String),
)

# Organisation model
organisations = Table(
    "organisations",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid4),
    Column("name", String, unique=True, index=True),
)

# Project model
projects = Table(
    "projects",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid4),
    Column("name", String, index=True),
    Column("organisation_id", UUID, ForeignKey("organisations.id")),
)

# Dataset model
datasets = Table(
    "datasets",
    metadata,
    Column("id", UUID, primary_key=True, default=uuid4),
    Column("name", String, index=True),
    Column("project_id", UUID, ForeignKey("projects.id")),
)

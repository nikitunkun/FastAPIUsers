import uuid

from sqlalchemy import Column, DateTime, String, Table
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.apps.base.models.metadata import Metadata

USER_TITLE = "user"


User = Table(
    USER_TITLE,
    Metadata.get(),
    Column(
        "id",
        UUID(as_uuid=False),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        comment="UUID",
    ),
    Column("username", String(128), unique=True, nullable=False, comment="Имя пользователя"),
    Column("password", String(128), unique=False, nullable=False, comment="Пароль пользователя"),
    Column("created_at", DateTime(timezone=True), server_default=func.now(), comment="Дата и время создания записи"),
    Column("updated_at", DateTime(timezone=True), onupdate=func.now(), comment="Дата и время обновления записи"),
)

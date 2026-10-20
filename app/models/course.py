from datetime import datetime

from sqlalchemy import DateTime, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

from pgvector.sqlalchemy import Vector

class Course(Base):
    __tablename__="courses"

    id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    provider: Mapped[str | None] = mapped_column(String(150), nullable=True)

    url: Mapped[str | None] = mapped_column(String(2048), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    embedding: Mapped[list[float]|None]=mapped_column(Vector(384),nullable=True,)
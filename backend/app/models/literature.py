import enum
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import UUIDModel


class LiteratureStatus(str, enum.Enum):  # noqa: UP042
    NOT_REVIEWED = "not_reviewed"
    READING = "reading"
    REVIEWED = "reviewed"


class Literature(UUIDModel):
    __tablename__ = "literature"

    question_id: Mapped[UUID] = mapped_column(
        ForeignKey("research_questions.id", ondelete="CASCADE"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(500))
    authors: Mapped[str | None] = mapped_column(String(1000))
    year: Mapped[int | None] = mapped_column(Integer)
    journal: Mapped[str | None] = mapped_column(String(500))
    doi: Mapped[str | None] = mapped_column(String(255))
    url: Mapped[str | None] = mapped_column(String(2048))
    abstract: Mapped[str | None] = mapped_column(Text())
    notes: Mapped[str | None] = mapped_column(Text())
    citation: Mapped[str | None] = mapped_column(Text())
    status: Mapped[LiteratureStatus] = mapped_column(
        Enum(
            LiteratureStatus,
            values_callable=lambda statuses: [status.value for status in statuses],
        ),
        default=LiteratureStatus.NOT_REVIEWED,
    )

    question = relationship("ResearchQuestion", back_populates="literature")

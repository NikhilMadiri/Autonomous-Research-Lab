import enum
from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import UUIDModel
class QuestionStatus(str, enum.Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    ANSWERED = "answered"
    ARCHIVED = "archived"
class ResearchQuestion(UUIDModel):
    __tablename__ = "research_questions"
    project_id: Mapped[object] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(240))
    description: Mapped[str | None] = mapped_column(Text())
    status: Mapped[QuestionStatus] = mapped_column(Enum(QuestionStatus), default=QuestionStatus.OPEN)
    project = relationship("Project", back_populates="questions")


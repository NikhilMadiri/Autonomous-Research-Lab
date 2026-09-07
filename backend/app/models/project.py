import enum

from sqlalchemy import Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import UUIDModel


class ProjectStatus(str, enum.Enum):  # noqa: UP042
    DRAFT = "draft"
    ACTIVE = "active"
    ARCHIVED = "archived"


class Project(UUIDModel):
    __tablename__ = "projects"
    owner_id: Mapped[object | None] = mapped_column(ForeignKey("users.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(160), index=True)
    description: Mapped[str | None] = mapped_column(Text())
    status: Mapped[ProjectStatus] = mapped_column(
        Enum( ProjectStatus,
        values_callable=lambda enum: [e.value for e in enum],
        name="projectstatus",),
        default=ProjectStatus.DRAFT,
    )
    owner = relationship("User", back_populates="projects")
    questions = relationship(
        "ResearchQuestion",
        back_populates="project",
        cascade="all, delete-orphan",
    )

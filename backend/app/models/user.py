import enum
from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import UUIDModel
class UserStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
class User(UUIDModel):
    __tablename__ = "users"
    email: Mapped[str] = mapped_column(String(320), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(120))
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), default=UserStatus.ACTIVE)
    projects = relationship("Project", back_populates="owner")


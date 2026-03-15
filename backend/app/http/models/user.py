import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship

from app.database.connection import Base


def now_utc():
    return datetime.now(timezone.utc)

# Role
class RoleEnum(str, enum.Enum):
    admin      = "admin"
    cashier    = "cashier"
    supervisor = "supervisor"

# Gender
class GenderEnum(str, enum.Enum):
    male   = "male"
    female = "female"

# Model
class User(Base):
    __tablename__ = "users"

    id_user    = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username   = Column(String(50), unique=True, nullable=False, index=True)
    email      = Column(String(100), unique=True, nullable=False, index=True)
    password   = Column(String(255), nullable=False)
    is_active  = Column(Boolean, default=True, nullable=False)

    created_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)
    updatet_at = Column(DateTime(timezone=True), default=now_utc, onupdate=now_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    # Relasi
    detail     = relationship("UserDetail", back_populates="user", uselist=False, cascade="all, delete-orphan")

    

    def __repr__(self):
        return f"<User id={self.id_user} username={self.username}>"
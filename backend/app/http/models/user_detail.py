from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Enum, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.database.connection import Base
from app.http.models.user import RoleEnum, GenderEnum

def now_utc():
    return datetime.now(timezone.utc)

# Model
class UserDetail(Base):
    __tablename__="user_details"

    id_detail  = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_user    = Column(Integer, ForeignKey("users.id_user", ondelete="CASCADE"), nullable=False, unique=True)
    full_name  = Column(String(100), nullable=False)
    gender     = Column(Enum(GenderEnum), nullable=True)
    phone      = Column(String(20), nullable=True)
    address    = Column(Text, nullable=True)
    role       = Column(Enum(RoleEnum), nullable=False, default=RoleEnum.cashier)

    created_at = Column(DateTime(timezone=True), default=now_utc, nullable=False)
    updatet_at = Column(DateTime(timezone=True), default=now_utc, onupdate=now_utc, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=True, default=None)

    # Relasi
    user       = relationship("User", back_populates="detail")

    def __repr__(self):
        return f"<UserDetail id={self.id_detail} full_name={self.full_name} role={self.role}>"
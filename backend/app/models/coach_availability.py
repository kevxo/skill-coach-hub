from datetime import time


from uuid import UUID


import uuid
from sqlalchemy import Column, Integer, Time, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base import Base

class CoachAvailability(Base):
    __tablename__ = "coach_availability"

    id = Column[UUID](UUID[UUID](as_uuid=True), primary_key=True, default=uuid.uuid4)

    coach_id = Column[UUID](UUID[UUID](as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    day_of_week = Column[int](Integer, nullable=False)
    start_time = Column[time](Time, nullable=False)
    end_time = Column[time](Time, nullable=False)

    coach = relationship("User", back_populates="availability")


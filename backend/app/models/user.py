from uuid import UUID
from typing import Any

import uuid
from sqlalchemy import Column, String, Enum
from app.db.base import Base
from sqlalchemy.dialects.postgresql import UUID
import enum

class UserRole(str,enum.Enum):
    player = "player"
    coach = "coach"

class User(Base):
    __tablename__ = "users"

    id = Column[Any](UUID[UUID](as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column[str](String, unique=True, index=True, nullable=False)
    password = Column[str](String, nullable=False)
    role = Column[UserRole](Enum(UserRole, name="userrole"), nullable=False)
    first_name = Column[str](String, nullable=False)
    last_name = Column[str](String, nullable=False)
    avatar_url = Column[str](String, nullable=True)
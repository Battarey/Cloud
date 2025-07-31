from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from sqlalchemy import ForeignKey, Text

Base = declarative_base()

class UserKey(Base):
    __tablename__ = "user_keys"
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    encrypted_key = Column(Text, nullable=False)

from sqlalchemy import Column, String, Boolean, Integer, BigInteger
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String(32), unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    files_count = Column(Integer, nullable=False, default=0)
    files_size = Column(BigInteger, nullable=False, default=0)
    free_space = Column(BigInteger, nullable=False, default=10*1024*1024*1024)  # 10 ГБ

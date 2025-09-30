from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, ForeignKey, JSON, Enum
)
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import enum
import uuid

Base = declarative_base()

class VisibilityEnum(str, enum.Enum):
    PUBLIC = "public"
    PERSONAL = "personal"
    PRIVATE = "private"
    SECURE = "secure"

class Journal(Base):
    __tablename__ = "journals"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(String, nullable=False)  # MongoDB user_id
    profile_id = Column(String, nullable=True)  # MongoDB profile_id
    s3_key = Column(String, nullable=False)
    title = Column(String, nullable=True)
    content_summary = Column(String, nullable=True)
    visibility = Column(Enum(VisibilityEnum), default=VisibilityEnum.PERSONAL)
    canonical_time = Column(DateTime(timezone=True), server_default=func.now())
    ingestion_source = Column(String, nullable=True)
    encryption_meta = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class JournalMetadata(Base):
    __tablename__ = "journal_metadata"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    journal_id = Column(UUID(as_uuid=True), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    tags = Column(ARRAY(String), nullable=True)
    mood = Column(String, nullable=True)
    feelings = Column(JSON, nullable=True)
    location = Column(JSON, nullable=True)
    device_info = Column(JSON, nullable=True)
    ingestion_source = Column(String, nullable=True)
    embeddings = Column(ARRAY(String), nullable=True)  # Store embeddings as array of floats (convert later)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

# Similarly define Recommendations, Insights, Notifications, Features

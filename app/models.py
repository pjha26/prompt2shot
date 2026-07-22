from datetime import datetime
from sqlalchemy import Column, String, Text, Enum, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
import uuid
import enum

Base = declarative_base()

class JobStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    completed = "completed"
    failed = "failed"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    reference_image_url = Column(String, nullable=True)
    status = Column(Enum(JobStatus), default=JobStatus.pending, nullable=False)
    generated_prompt = Column(Text, nullable=True)
    image_url = Column(String, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

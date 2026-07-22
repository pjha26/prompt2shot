from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from uuid import UUID
from app.models import JobStatus

# Request schema for creating a job
class GenerateRequest(BaseModel):
    product_name: str
    description: str
    reference_image_url: Optional[str] = None

# Response schema for a job
class JobResponse(BaseModel):
    id: UUID
    product_name: str
    description: str
    reference_image_url: Optional[str]
    status: JobStatus
    generated_prompt: Optional[str]
    image_url: Optional[str]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Lightweight schema for the job list (GET /jobs)
class JobListItem(BaseModel):
    id: UUID
    product_name: str
    status: JobStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

import pathlib
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
import uuid

from app.database import get_db
from app.models import Job, JobStatus
from app.schemas import GenerateRequest, JobResponse, JobListItem
from app.queue import generation_queue
from app.worker_tasks import process_job

app = FastAPI(
    title="Prompt2Shot Engine",
    description="Service that takes product info and generates AI creative images.",
    version="0.1.0"
)

# --- Static file serving ---
# Resolve the static/ directory relative to the project root (one level up from app/)
STATIC_DIR = pathlib.Path(__file__).resolve().parent.parent / "static"

# Mount the static directory so CSS/JS/images can be loaded via /static/...
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/")
async def root():
    """Serve the frontend HTML page."""
    return FileResponse(str(STATIC_DIR / "index.html"))


@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint to ensure the service is running
    and can connect to the database.
    """
    try:
        # Simple query to verify database connection
        await db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as e:
        # If the database is unreachable, return a 503 Service Unavailable
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Database connection failed: {str(e)}"
        )


@app.get("/jobs", response_model=List[JobListItem])
async def list_jobs(db: AsyncSession = Depends(get_db)):
    """
    Returns all jobs ordered by created_at descending (most recent first).
    Used by the frontend to populate the job list on page load.
    """
    stmt = select(Job).order_by(Job.created_at.desc())
    result = await db.execute(stmt)
    jobs = result.scalars().all()
    return jobs


@app.post("/generate", status_code=status.HTTP_202_ACCEPTED)
async def generate_image(request: GenerateRequest, db: AsyncSession = Depends(get_db)):
    """
    Creates a new image generation job and enqueues it for background processing.
    Returns the job_id immediately.
    """
    product_name = request.product_name.strip()
    description = request.description.strip()
    
    if not product_name or not description:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Product name and description cannot be empty or whitespace only"
        )
        
    if len(product_name) > 500:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Product name exceeds maximum length of 500 characters"
        )
        
    if len(description) > 2000:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Description exceeds maximum length of 2000 characters"
        )

    # 1. Create a job row in Postgres with status "pending"
    job = Job(
        product_name=product_name,
        description=description,
        reference_image_url=request.reference_image_url,
        status=JobStatus.pending
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    # 2. Enqueue the job to the RQ queue
    generation_queue.enqueue(process_job, str(job.id))
    
    # 3. Return job_id immediately
    return {"job_id": job.id}


@app.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job(job_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Fetches the current status and details of a job by its ID.
    """
    stmt = select(Job).where(Job.id == job_id)
    result = await db.execute(stmt)
    job = result.scalar_one_or_none()
    
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Job not found"
        )
        
    return job

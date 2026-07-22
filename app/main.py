from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select
import uuid

from app.database import get_db
from app.models import Job, JobStatus
from app.schemas import GenerateRequest, JobResponse
from app.queue import generation_queue
from app.worker_tasks import process_job

app = FastAPI(
    title="Prompt2Shot Engine",
    description="Service that takes product info and generates AI creative images.",
    version="0.1.0"
)

@app.get("/")
async def root():
    return {"message": "Welcome to Prompt2Shot Engine"}

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

@app.post("/generate", status_code=status.HTTP_202_ACCEPTED)
async def generate_image(request: GenerateRequest, db: AsyncSession = Depends(get_db)):
    """
    Creates a new image generation job and enqueues it for background processing.
    Returns the job_id immediately.
    """
    # 1. Create a job row in Postgres with status "pending"
    job = Job(
        product_name=request.product_name,
        description=request.description,
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

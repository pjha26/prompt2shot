import asyncio
import logging
from groq import AsyncGroq
from sqlalchemy import select
from app.database import AsyncSessionLocal
from app.models import Job, JobStatus
from app.config import settings
from app.image_gen import generate_image

logger = logging.getLogger(__name__)

async def process_job_async(job_id: str):
    """
    Asynchronous implementation of the job processing logic.
    """
    async with AsyncSessionLocal() as session:
        # Fetch the job
        stmt = select(Job).where(Job.id == job_id)
        result = await session.execute(stmt)
        job = result.scalar_one_or_none()

        if not job:
            logger.error(f"Job {job_id} not found in database.")
            return

        try:
            # Set status to processing
            job.status = JobStatus.processing
            await session.commit()
            
            # 1. Generate prompt via Groq LLM
            logger.info(f"Generating prompt for job {job_id}")
            groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)
            
            prompt_instruction = (
                f"Given this product name and description, write a concise, vivid "
                f"image-generation prompt describing lighting, styling, and mood "
                f"for a professional product photo.\n\n"
                f"Product Name: {job.product_name}\n"
                f"Description: {job.description}"
            )
            
            generated_prompt = None
            for attempt in range(2):
                try:
                    completion = await asyncio.wait_for(
                        groq_client.chat.completions.create(
                            messages=[
                                {
                                    "role": "user",
                                    "content": prompt_instruction,
                                }
                            ],
                            model="llama-3.1-8b-instant",  # Fast model for prompt generation
                            temperature=0.7,
                            max_tokens=256,
                        ),
                        timeout=20.0
                    )
                    content = completion.choices[0].message.content.strip()
                    if content:
                        generated_prompt = content
                        break
                except Exception as e:
                    logger.warning(f"Groq API attempt {attempt + 1} failed: {str(e)}")
                    if attempt == 1:
                        logger.error("Groq API failed after retry. Using fallback prompt.")
            
            if not generated_prompt:
                generated_prompt = f"Professional product photograph of {job.product_name}, {job.description}, studio lighting, high quality"
                
            job.generated_prompt = generated_prompt
            
            # 2. Call image generation API
            logger.info(f"Generating image for job {job_id}")
            image_url = await generate_image(generated_prompt)
            job.image_url = image_url
            
            # 3. Mark job as completed
            job.status = JobStatus.completed
            await session.commit()
            logger.info(f"Job {job_id} completed successfully.")
            
        except Exception as e:
            error_msg = str(e) or type(e).__name__
            logger.error(f"Error processing job {job_id}: {error_msg}")
            job.status = JobStatus.failed
            job.error_message = f"Job failed during processing: {error_msg}"
            await session.commit()

def process_job(job_id: str):
    """
    Synchronous entrypoint for RQ worker.
    Runs the async logic within a new event loop.
    """
    asyncio.run(process_job_async(job_id))

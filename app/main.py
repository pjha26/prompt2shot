from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.database import get_db

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

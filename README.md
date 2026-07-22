# Prompt2Shot Engine

This is the FastAPI backend for the Prompt2Shot service, which takes product information and generates AI creative images via an async job pipeline using Redis and RQ.

## Prerequisites

- Python 3.10+
- PostgreSQL database
- Redis (Local or Upstash free tier)
- Groq API Key (for LLM prompt generation)

## Setup Instructions

1. **Clone the repository and set up a virtual environment**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   - Copy the `.env.example` file to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit the `.env` file with your credentials:
     - `DATABASE_URL`: Must use the `asyncpg` driver (e.g., `postgresql+asyncpg://postgres:password@localhost:5432/prompt2shot`)
     - `REDIS_URL`: Connection to your Redis instance (e.g., `redis://localhost:6379/0` or your Upstash URL)
     - `GROQ_API_KEY`: Your Groq API key for prompt generation.

4. **Run Database Migrations**
   This project uses Alembic to manage database migrations. To create the initial tables, run:
   ```bash
   alembic upgrade head
   ```

5. **Start the Background Worker**
   In a separate terminal (with the virtual environment activated), start the RQ worker to process generation jobs:
   ```bash
   python worker.py
   ```

6. **Start the Development Server**
   In your main terminal, start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check endpoint (verifies database connection)
- `POST /generate`: Submit a new job to generate an image (returns immediately with a job ID)
- `GET /jobs/{job_id}`: Poll the status of a specific job

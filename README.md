# Prompt2Shot Engine

This is the FastAPI backend for the Prompt2Shot service, which takes product information and generates AI creative images via an async job pipeline.

## Prerequisites

- Python 3.10+
- PostgreSQL database

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
   - Edit the `.env` file and set the `DATABASE_URL` to point to your local PostgreSQL database. The format must use the `asyncpg` driver:
     ```
     DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/prompt2shot
     ```

4. **Run Database Migrations**
   This project uses Alembic to manage database migrations. To create the initial tables, run:
   ```bash
   alembic upgrade head
   ```

5. **Start the Development Server**
   ```bash
   uvicorn app.main:app --reload
   ```

## Endpoints

- `GET /`: Welcome message
- `GET /health`: Health check endpoint (verifies database connection)

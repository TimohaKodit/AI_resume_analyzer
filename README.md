# AI Resume Analyzer

Backend service for AI-powered resume analysis and vacancy matching.

## Features

- Upload PDF resume and get AI analysis powered by Google Gemini
- Search vacancies from Habr Career
- Compare resume with vacancy using LangChain + Gemini
- User authentication with JWT tokens
- Resume stored per user account in PostgreSQL

## Tech Stack

- **FastAPI** — web framework
- **LangChain + Google Gemini** — AI analysis
- **PostgreSQL + SQLAlchemy** — database
- **Alembic** — database migrations
- **JWT (python-jose)** — authentication
- **aiohttp + feedparser** — vacancy parsing from Habr Career

## Project Structure

```
app/
├── api/
│   ├── auth_router.py      # Registration and login endpoints
│   └── resume_router.py    # Resume upload and vacancy search
├── chains/
│   └── resume_chain.py     # LangChain chain for AI analysis
├── services/
│   ├── resume_parser.py    # PDF text extraction
│   ├── resume_service.py   # Resume analysis service
│   └── habr_client.py      # Habr Career vacancy parser
├── database.py             # SQLAlchemy async engine and session
├── models.py               # Database models
├── schemas.py              # Pydantic schemas
├── dependencies.py         # FastAPI dependencies
└── main.py                 # App entry point
```

## Setup

1. Clone the repository
2. Create virtual environment and install dependencies:
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

3. Create `.env` file:
```
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/resume_analyzer
SECRET_KEY=your_secret_key
HH_USER_AGENT=YourApp/1.0 (your@email.com)
```

4. Run database migrations:
```bash
alembic upgrade head
```

5. Start the server:
```bash
uvicorn app.main:app --reload
```

6. Open API docs at `http://localhost:8000/docs`

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| POST | `/analyze` | Upload PDF and get AI analysis |
| GET | `/vacancies?query=` | Search vacancies on Habr Career |

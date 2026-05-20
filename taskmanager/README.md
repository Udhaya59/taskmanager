# TaskFlow — Task Manager

A full-stack Task Manager application built with **FastAPI** (backend) and vanilla **HTML/CSS/JS** (frontend).

---

## Features

- **JWT Authentication** — Register, login, secure token-based sessions
- **Task CRUD** — Create, read, update (mark complete), delete tasks
- **Task Isolation** — Users only ever see their own tasks
- **Pagination** — Configurable page size (`?page=1&page_size=10`)
- **Filtering** — Filter by completion status (`?completed=true`)
- **Interactive Docs** — Auto-generated at `/docs` (Swagger UI)
- **Single-file Frontend** — No build step; served directly by FastAPI
- **Pytest Suite** — Auth + task tests with isolated test database

---

## Project Structure

```
taskmanager/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py        # Pydantic settings
│   │   │   ├── security.py      # JWT & bcrypt helpers
│   │   │   └── dependencies.py  # get_current_user dependency
│   │   ├── db/
│   │   │   └── database.py      # SQLAlchemy engine & session
│   │   ├── models/
│   │   │   └── models.py        # User & Task ORM models
│   │   ├── routers/
│   │   │   ├── auth.py          # POST /register, POST /login
│   │   │   └── tasks.py         # Full CRUD /tasks
│   │   ├── schemas/
│   │   │   └── schemas.py       # Pydantic request/response models
│   │   └── main.py              # FastAPI app, CORS, static files
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   └── test_tasks.py
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   └── index.html               # Single-page app (no build step)
├── Dockerfile
├── render.yaml
└── README.md
```

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/register` | ✗ | Create a new account |
| POST | `/login` | ✗ | Login, get JWT token |
| POST | `/tasks` | ✓ | Create a task |
| GET | `/tasks` | ✓ | List tasks (paginated, filterable) |
| GET | `/tasks/{id}` | ✓ | Get a specific task |
| PUT | `/tasks/{id}` | ✓ | Update / mark as completed |
| DELETE | `/tasks/{id}` | ✓ | Delete a task |
| GET | `/docs` | ✗ | Swagger UI |
| GET | `/health` | ✗ | Health check |

**Query params for `GET /tasks`:**
- `?page=1` — page number (default: 1)
- `?page_size=10` — results per page (default: 10, max: 100)
- `?completed=true` — filter by completed status
- `?completed=false` — filter by pending status

---

## Environment Variables

Copy `.env.example` to `.env` and fill in values:

```env
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./taskmanager.db
```

> **Never commit `.env` to version control.**

---

## Running Locally

### Prerequisites
- Python 3.11+
- pip

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/taskflow.git
cd taskflow

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Copy env file
cp .env.example .env
# Edit .env with your values

# Run the server (from the backend/ directory)
uvicorn app.main:app --reload --port 8000
```

Open your browser at:
- **App**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Running Tests

```bash
cd backend
pytest tests/ -v
```

---

## Docker

```bash
# Build image
docker build -t taskflow .

# Run container
docker run -p 8000:8000 -e SECRET_KEY=mysecret taskflow
```

---

## Deployment (Render)

1. Push your code to a public GitHub repository
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your GitHub repo
4. Render auto-detects `render.yaml` and configures the service
5. Set environment variables in the Render dashboard (especially `SECRET_KEY`)
6. Deploy — your app will be live at `https://your-app.onrender.com`

The `/docs` endpoint is always accessible after deployment.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend framework | FastAPI |
| ORM | SQLAlchemy |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Validation | Pydantic v2 |
| Testing | pytest + httpx |
| Frontend | Vanilla HTML/CSS/JS |
| Containerization | Docker |
| Deployment | Render |

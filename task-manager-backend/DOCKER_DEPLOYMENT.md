# Task Manager API - Production-Ready Backend

A **production-ready** and **cloud-ready** RESTful API for task management built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, **Alembic**, and **Docker**.

## 🎯 New Production Features

- ✅ **Docker & Docker Compose** - Containerized deployment
- ✅ **Structured Logging** - File and console logging with levels
- ✅ **Exception Middleware** - Centralized error handling
- ✅ **Environment Management** - Development/Production configs
- ✅ **Unit Tests** - Comprehensive pytest test suite
- ✅ **Health Checks** - Docker and API health monitoring
- ✅ **CORS Configuration** - Cross-origin resource sharing
- ✅ **Security** - Non-root Docker user, secrets management

## 📋 Features

- ✅ Full CRUD operations for tasks
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Database migrations with Alembic
- ✅ Request/response validation with Pydantic
- ✅ Pagination and filtering support
- ✅ Interactive API documentation (Swagger/ReDoc)
- ✅ Production-ready Docker setup
- ✅ Comprehensive test coverage

## 🏗️ Project Structure

```
task-manager-backend/
│
├── alembic/                    # Database migrations
│   ├── versions/
│   │   └── 001_initial_migration.py
│   ├── env.py
│   └── script.py.mako
│
├── app/                        # Application code
│   ├── api/                    # API routes
│   │   └── tasks.py
│   │
│   ├── core/                   # Core configuration
│   │   ├── config.py           # Settings & environment
│   │   ├── logging.py          # Logging configuration
│   │   └── middleware.py       # Exception handlers
│   │
│   ├── db/                     # Database layer
│   │   ├── database.py
│   │   └── models.py
│   │
│   ├── crud.py                 # CRUD operations
│   ├── main.py                 # FastAPI application
│   └── schemas.py              # Pydantic schemas
│
├── tests/                      # Unit tests
│   ├── conftest.py             # Pytest fixtures
│   └── test_tasks.py           # Task endpoint tests
│
├── logs/                       # Application logs (auto-created)
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml          # Production setup
├── docker-compose.dev.yml      # Development setup
├── Dockerfile
├── pytest.ini
├── README.md
└── requirements.txt
```

## 🚀 Quick Start with Docker (Recommended)

### Prerequisites

- Docker Desktop installed
- Docker Compose installed

### 1️⃣ Clone and Configure

```powershell
cd C:\Users\chieu\Desktop\R\Cloud\task-manager-backend

# Copy environment file
copy .env.example .env
```

### 2️⃣ Start with Docker Compose

**Production Mode:**

```powershell
docker-compose up --build
```

**Development Mode (with hot reload):**

```powershell
docker-compose -f docker-compose.dev.yml up --build
```

### 3️⃣ Access the API

- **API Base**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 4️⃣ Stop Services

```powershell
docker-compose down

# Remove volumes (delete database data)
docker-compose down -v
```

## 💻 Local Development Setup (Without Docker)

### Prerequisites

- Python 3.10+
- PostgreSQL 12+

### 1️⃣ Setup Environment

```powershell
# Create virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2️⃣ Configure Database

```powershell
# Create database
psql -U postgres -c "CREATE DATABASE taskmanager;"

# Copy and edit environment file
copy .env.example .env
# Edit .env with your database credentials
```

### 3️⃣ Run Migrations

```powershell
alembic upgrade head
```

### 4️⃣ Start Server

```powershell
# Development mode
uvicorn app.main:app --reload

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 🧪 Running Tests

### Run All Tests

```powershell
# Activate virtual environment first
.\venv\Scripts\Activate.ps1

# Run tests with coverage
pytest

# Run tests with verbose output
pytest -v

# Run specific test file
pytest tests/test_tasks.py

# Run specific test
pytest tests/test_tasks.py::TestTaskCreate::test_create_task_success
```

### View Coverage Report

```powershell
# Generate HTML coverage report
pytest --cov=app --cov-report=html

# Open report
start htmlcov/index.html
```

## 🔧 Configuration

### Environment Variables

Edit `.env` file:

```env
# Application
ENV=development              # development, staging, production
DEBUG=True                   # Enable debug mode
LOG_LEVEL=INFO              # DEBUG, INFO, WARNING, ERROR, CRITICAL

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/taskmanager

# CORS (comma-separated or *)
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# Security
SECRET_KEY=your-secret-key-change-in-production
```

### Docker Environment

For Docker deployments, update environment variables in `docker-compose.yml`:

```yaml
environment:
  DATABASE_URL: postgresql://postgres:postgres@db:5432/taskmanager
  ENV: production
  DEBUG: "false"
  LOG_LEVEL: INFO
  CORS_ORIGINS: "*"
```

## 📊 Logging

Logs are stored in the `logs/` directory:

- **app.log** - All application logs
- **error.log** - Error-level logs only

Log format:

```
2025-11-22 10:30:45 - app.main - INFO - Starting Task Manager API v1.0.0
2025-11-22 10:30:46 - app.api.tasks - INFO - Incoming request: GET /api/v1/tasks
```

### Log Levels

- **DEBUG** - Detailed information for debugging
- **INFO** - General informational messages
- **WARNING** - Warning messages
- **ERROR** - Error messages
- **CRITICAL** - Critical issues

## 🛡️ Error Handling

The API returns consistent error responses:

### 404 Not Found

```json
{
  "error": {
    "status_code": 404,
    "message": "Task with id 123 not found",
    "path": "/api/v1/tasks/123"
  }
}
```

### 422 Validation Error

```json
{
  "error": {
    "status_code": 422,
    "message": "Validation error",
    "path": "/api/v1/tasks",
    "details": [...]
  }
}
```

### 500 Internal Server Error

```json
{
  "error": {
    "status_code": 500,
    "message": "Internal server error",
    "path": "/api/v1/tasks"
  }
}
```

## 📚 API Endpoints

| Method   | Endpoint                      | Description               |
| -------- | ----------------------------- | ------------------------- |
| `GET`    | `/`                           | Root endpoint             |
| `GET`    | `/health`                     | Health check              |
| `GET`    | `/api/v1/tasks`               | Get all tasks (paginated) |
| `GET`    | `/api/v1/tasks/{id}`          | Get task by ID            |
| `POST`   | `/api/v1/tasks`               | Create new task           |
| `PUT`    | `/api/v1/tasks/{id}`          | Update task               |
| `DELETE` | `/api/v1/tasks/{id}`          | Delete task               |
| `GET`    | `/api/v1/tasks/stats/summary` | Get statistics            |

## 🐳 Docker Commands

### Build and Run

```powershell
# Build image
docker build -t taskmanager-api .

# Run container
docker run -p 8000:8000 --env-file .env taskmanager-api

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f api

# Execute commands in container
docker-compose exec api bash
docker-compose exec api alembic upgrade head
```

### Cleanup

```powershell
# Stop containers
docker-compose down

# Remove volumes
docker-compose down -v

# Remove images
docker rmi taskmanager-api
```

## 🔄 Database Migrations

### Create New Migration

```powershell
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Add new column"

# Create empty migration
alembic revision -m "Custom migration"
```

### Apply Migrations

```powershell
# Upgrade to latest
alembic upgrade head

# Downgrade one revision
alembic downgrade -1

# Check current version
alembic current

# View history
alembic history
```

## 📝 API Usage Examples

### Create Task

```powershell
$body = @{
    title = "Complete documentation"
    description = "Write comprehensive API docs"
    status = "pending"
    priority = "high"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks" `
    -Method Post -Body $body -ContentType "application/json"
```

### Get All Tasks

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks?page=1&page_size=10"
```

### Update Task

```powershell
$body = @{
    status = "completed"
    completed = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks/1" `
    -Method Put -Body $body -ContentType "application/json"
```

### Delete Task

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks/1" -Method Delete
```

## 🚀 Production Deployment

### 1. Update Environment

```env
ENV=production
DEBUG=False
LOG_LEVEL=WARNING
CORS_ORIGINS=https://yourdomain.com
SECRET_KEY=use-strong-random-secret-key
```

### 2. Build Production Image

```powershell
docker build -t taskmanager-api:latest .
```

### 3. Deploy with Docker Compose

```powershell
docker-compose -f docker-compose.yml up -d
```

### 4. Run Migrations

```powershell
docker-compose exec api alembic upgrade head
```

### 5. Monitor Logs

```powershell
docker-compose logs -f
```

## 🔒 Security Considerations

- ✅ Non-root Docker user
- ✅ Environment-based secrets
- ✅ CORS configuration
- ✅ Request validation
- ✅ SQL injection protection (SQLAlchemy)
- ✅ Structured error responses
- ⚠️ Add authentication/authorization for production
- ⚠️ Use HTTPS in production
- ⚠️ Implement rate limiting

## 🧰 Development Tools

```powershell
# Format code
black app/ tests/

# Lint code
flake8 app/ tests/

# Type checking
mypy app/

# Run all quality checks
black app/ tests/; flake8 app/ tests/; pytest
```

## 📈 Monitoring

### Health Check

```powershell
curl http://localhost:8000/health
```

### Docker Health Check

```powershell
docker inspect taskmanager-api | Select-String -Pattern "Health"
```

### Database Connection

```powershell
docker-compose exec db psql -U postgres -d taskmanager -c "\dt"
```

## 🐛 Troubleshooting

### Database Connection Issues

```powershell
# Check database is running
docker-compose ps db

# Test connection
docker-compose exec db psql -U postgres -c "SELECT version();"
```

### Port Already in Use

```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

### View Application Logs

```powershell
# Docker logs
docker-compose logs api

# Local logs
Get-Content logs/app.log -Tail 50

# Error logs only
Get-Content logs/error.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `pytest`
5. Format code: `black .`
6. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Author

Created with FastAPI, PostgreSQL, Docker, and ❤️

---

**Happy Coding! 🚀**

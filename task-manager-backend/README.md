# Task Manager API - FastAPI Backend

A production-ready RESTful API for task management built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **Alembic**.

## 📋 Features

- ✅ Full CRUD operations for tasks
- ✅ PostgreSQL database with SQLAlchemy ORM
- ✅ Database migrations with Alembic
- ✅ Request/response validation with Pydantic
- ✅ Pagination support
- ✅ Filtering by status, priority, and completion
- ✅ Comprehensive error handling
- ✅ Interactive API documentation (Swagger/ReDoc)
- ✅ CORS support
- ✅ Production-ready structure

## 🏗️ Project Structure

```
task-manager-backend/
│
├── alembic/                    # Database migrations
│   ├── versions/               # Migration files
│   │   └── 001_initial_migration.py
│   ├── env.py                  # Alembic environment config
│   └── script.py.mako          # Migration template
│
├── app/                        # Application code
│   ├── api/                    # API routes
│   │   ├── __init__.py
│   │   └── tasks.py            # Task endpoints
│   │
│   ├── core/                   # Core configuration
│   │   ├── __init__.py
│   │   └── config.py           # Settings and config
│   │
│   ├── db/                     # Database layer
│   │   ├── __init__.py
│   │   ├── database.py         # DB connection
│   │   └── models.py           # SQLAlchemy models
│   │
│   ├── __init__.py
│   ├── crud.py                 # CRUD operations
│   ├── main.py                 # FastAPI application
│   └── schemas.py              # Pydantic schemas
│
├── .env.example                # Example environment variables
├── .gitignore                  # Git ignore file
├── alembic.ini                 # Alembic configuration
├── README.md                   # This file
└── requirements.txt            # Python dependencies
```

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 12 or higher
- pip (Python package manager)

### Step 1: Clone and Navigate

```powershell
cd C:\Users\chieu\Desktop\R\Cloud\task-manager-backend
```

### Step 2: Create Virtual Environment

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies

```powershell
pip install -r requirements.txt
```

### Step 4: Create PostgreSQL Database

**Option A: Using psql (PostgreSQL CLI)**

```powershell
# Connect to PostgreSQL
psql -U postgres

# In PostgreSQL prompt:
CREATE DATABASE taskmanager;
\q
```

**Option B: Using pgAdmin**

1. Open pgAdmin
2. Right-click on "Databases"
3. Select "Create" → "Database"
4. Name: `taskmanager`
5. Click "Save"

### Step 5: Configure Environment Variables

```powershell
# Copy example env file
copy .env.example .env
```

Edit `.env` and update the database connection:

```env
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/taskmanager
DEBUG=True
```

### Step 6: Run Database Migrations

```powershell
# Apply migrations to create tables
alembic upgrade head
```

**To verify tables were created:**

```powershell
psql -U postgres -d taskmanager -c "\dt"
```

### Step 7: Start the FastAPI Server

```powershell
# Development mode with auto-reload
uvicorn app.main:app --reload

# Or run directly
python -m app.main
```

The API will be available at:

- **API Base URL**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## 📚 API Endpoints

### Task Management

| Method   | Endpoint                      | Description                               |
| -------- | ----------------------------- | ----------------------------------------- |
| `GET`    | `/api/v1/tasks`               | Get all tasks (with pagination & filters) |
| `GET`    | `/api/v1/tasks/{task_id}`     | Get a specific task                       |
| `POST`   | `/api/v1/tasks`               | Create a new task                         |
| `PUT`    | `/api/v1/tasks/{task_id}`     | Update a task                             |
| `DELETE` | `/api/v1/tasks/{task_id}`     | Delete a task                             |
| `GET`    | `/api/v1/tasks/stats/summary` | Get task statistics                       |

### Other Endpoints

| Method | Endpoint  | Description   |
| ------ | --------- | ------------- |
| `GET`  | `/`       | Root endpoint |
| `GET`  | `/health` | Health check  |

## 🔧 API Usage Examples

### 1. Create a Task

```powershell
# Using PowerShell
$body = @{
    title = "Complete project documentation"
    description = "Write comprehensive README and API docs"
    status = "pending"
    priority = "high"
    completed = $false
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks" -Method Post -Body $body -ContentType "application/json"
```

**cURL equivalent:**

```bash
curl -X POST "http://localhost:8000/api/v1/tasks" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Complete project documentation",
    "description": "Write comprehensive README and API docs",
    "status": "pending",
    "priority": "high",
    "completed": false
  }'
```

### 2. Get All Tasks (with pagination)

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks?page=1&page_size=10"
```

### 3. Get Tasks with Filters

```powershell
# Filter by status
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks?status=pending"

# Filter by priority
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks?priority=high"

# Filter by completion status
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks?completed=false"
```

### 4. Get a Specific Task

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks/1"
```

### 5. Update a Task

```powershell
$body = @{
    status = "completed"
    completed = $true
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks/1" -Method Put -Body $body -ContentType "application/json"
```

### 6. Delete a Task

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks/1" -Method Delete
```

### 7. Get Task Statistics

```powershell
Invoke-RestMethod -Uri "http://localhost:8000/api/v1/tasks/stats/summary"
```

## 🗄️ Database Schema

### Tasks Table

| Column        | Type        | Constraints                  | Description            |
| ------------- | ----------- | ---------------------------- | ---------------------- |
| `id`          | Integer     | Primary Key, Auto-increment  | Unique task identifier |
| `title`       | String(255) | Not Null, Indexed            | Task title             |
| `description` | Text        | Nullable                     | Task description       |
| `status`      | String(50)  | Not Null, Default: 'pending' | Task status            |
| `priority`    | String(50)  | Not Null, Default: 'medium'  | Task priority          |
| `completed`   | Boolean     | Not Null, Default: False     | Completion flag        |
| `created_at`  | DateTime    | Not Null, Auto-generated     | Creation timestamp     |
| `updated_at`  | DateTime    | Not Null, Auto-updated       | Last update timestamp  |

## 🔄 Database Migrations with Alembic

### Check Current Migration Status

```powershell
alembic current
```

### Create a New Migration

```powershell
# Auto-generate migration from model changes
alembic revision --autogenerate -m "Description of changes"
```

### Apply Migrations

```powershell
# Upgrade to latest
alembic upgrade head

# Upgrade to specific revision
alembic upgrade <revision_id>
```

### Rollback Migrations

```powershell
# Downgrade one revision
alembic downgrade -1

# Downgrade to specific revision
alembic downgrade <revision_id>
```

### View Migration History

```powershell
alembic history --verbose
```

## 🧪 Testing

### Manual Testing with Swagger UI

1. Start the server: `uvicorn app.main:app --reload`
2. Open browser: http://localhost:8000/docs
3. Use the interactive interface to test endpoints

### Using pytest (Future)

```powershell
pytest
```

## 📦 Production Deployment

### Update Production Settings

Edit `.env` for production:

```env
DATABASE_URL=postgresql://user:password@production-host:5432/taskmanager
DEBUG=False
BACKEND_CORS_ORIGINS=https://yourdomain.com
```

### Run with Production Server

```powershell
# Using Gunicorn with Uvicorn workers (Linux/Mac)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Using Uvicorn directly (Windows/Development)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Docker Deployment (Optional)

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```powershell
docker build -t task-manager-api .
docker run -p 8000:8000 --env-file .env task-manager-api
```

## 🛠️ Troubleshooting

### Database Connection Issues

```powershell
# Test PostgreSQL connection
psql -U postgres -d taskmanager -c "SELECT version();"
```

### Migration Issues

```powershell
# Reset database (CAUTION: Deletes all data!)
alembic downgrade base
alembic upgrade head
```

### Port Already in Use

```powershell
# Change port in command
uvicorn app.main:app --reload --port 8001
```

## 📝 Common Status and Priority Values

**Status Options:**

- `pending` - Task not started
- `in_progress` - Task in progress
- `completed` - Task finished

**Priority Options:**

- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 👥 Author

Created with FastAPI, PostgreSQL, and ❤️

---

**Happy Coding! 🚀**

"""
CRUD operations for Task model
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional
from app.db.models import Task
from app.schemas import TaskCreate, TaskUpdate


def get_task(db: Session, task_id: int) -> Optional[Task]:
    """
    Get a single task by ID
    
    Args:
        db: Database session
        task_id: Task ID
    
    Returns:
        Task object or None if not found
    """
    return db.query(Task).filter(Task.id == task_id).first()


def get_tasks(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    completed: Optional[bool] = None
) -> tuple[list[Task], int]:
    """
    Get all tasks with optional filtering and pagination
    
    Args:
        db: Database session
        skip: Number of records to skip
        limit: Maximum number of records to return
        status: Filter by status
        priority: Filter by priority
        completed: Filter by completion status
    
    Returns:
        Tuple of (list of tasks, total count)
    """
    query = db.query(Task)
    
    # Apply filters
    if status is not None:
        query = query.filter(Task.status == status)
    if priority is not None:
        query = query.filter(Task.priority == priority)
    if completed is not None:
        query = query.filter(Task.completed == completed)
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    tasks = query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()
    
    return tasks, total


def create_task(db: Session, task: TaskCreate) -> Task:
    """
    Create a new task
    
    Args:
        db: Database session
        task: Task creation data
    
    Returns:
        Created task object
    """
    db_task = Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task_update: TaskUpdate) -> Optional[Task]:
    """
    Update an existing task
    
    Args:
        db: Database session
        task_id: Task ID
        task_update: Task update data
    
    Returns:
        Updated task object or None if not found
    """
    db_task = get_task(db, task_id)
    if db_task is None:
        return None
    
    # Update only provided fields
    update_data = task_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int) -> bool:
    """
    Delete a task
    
    Args:
        db: Database session
        task_id: Task ID
    
    Returns:
        True if deleted, False if not found
    """
    db_task = get_task(db, task_id)
    if db_task is None:
        return False
    
    db.delete(db_task)
    db.commit()
    return True


def get_task_stats(db: Session) -> dict:
    """
    Get task statistics
    
    Args:
        db: Database session
    
    Returns:
        Dictionary with task statistics
    """
    total = db.query(func.count(Task.id)).scalar()
    completed = db.query(func.count(Task.id)).filter(Task.completed == True).scalar()
    pending = db.query(func.count(Task.id)).filter(Task.status == "pending").scalar()
    in_progress = db.query(func.count(Task.id)).filter(Task.status == "in_progress").scalar()
    
    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "in_progress": in_progress
    }

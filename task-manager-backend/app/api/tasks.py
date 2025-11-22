"""
API routes for task management
"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import Optional
import math

from app.db.database import get_db
from app.schemas import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskListResponse,
    MessageResponse
)
from app import crud

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=TaskListResponse, summary="Get all tasks")
def get_tasks(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Number of items per page"),
    status: Optional[str] = Query(None, description="Filter by status"),
    priority: Optional[str] = Query(None, description="Filter by priority"),
    completed: Optional[bool] = Query(None, description="Filter by completion status"),
    db: Session = Depends(get_db)
):
    """
    Retrieve all tasks with pagination and optional filters.
    
    - **page**: Page number (starts at 1)
    - **page_size**: Number of items per page (max 100)
    - **status**: Filter by status (pending, in_progress, completed)
    - **priority**: Filter by priority (low, medium, high)
    - **completed**: Filter by completion status
    """
    skip = (page - 1) * page_size
    
    tasks, total = crud.get_tasks(
        db=db,
        skip=skip,
        limit=page_size,
        status=status,
        priority=priority,
        completed=completed
    )
    
    total_pages = math.ceil(total / page_size) if total > 0 else 0
    
    return TaskListResponse(
        tasks=tasks,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )


@router.get("/{task_id}", response_model=TaskResponse, summary="Get a task by ID")
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Retrieve a specific task by ID.
    
    - **task_id**: The ID of the task to retrieve
    """
    db_task = crud.get_task(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return db_task


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED, summary="Create a new task")
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new task.
    
    - **title**: Task title (required)
    - **description**: Task description (optional)
    - **status**: Task status (default: pending)
    - **priority**: Task priority (default: medium)
    - **completed**: Completion status (default: false)
    """
    return crud.create_task(db=db, task=task)


@router.put("/{task_id}", response_model=TaskResponse, summary="Update a task")
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db)
):
    """
    Update an existing task.
    
    - **task_id**: The ID of the task to update
    - **title**: Updated task title (optional)
    - **description**: Updated task description (optional)
    - **status**: Updated task status (optional)
    - **priority**: Updated task priority (optional)
    - **completed**: Updated completion status (optional)
    """
    db_task = crud.update_task(db=db, task_id=task_id, task_update=task)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return db_task


@router.delete("/{task_id}", response_model=MessageResponse, summary="Delete a task")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a task.
    
    - **task_id**: The ID of the task to delete
    """
    success = crud.delete_task(db=db, task_id=task_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )
    return MessageResponse(message=f"Task {task_id} deleted successfully")


@router.get("/stats/summary", response_model=dict, summary="Get task statistics")
def get_task_stats(db: Session = Depends(get_db)):
    """
    Get task statistics including total, completed, pending, and in-progress counts.
    """
    return crud.get_task_stats(db=db)

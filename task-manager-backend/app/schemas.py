"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class TaskBase(BaseModel):
    """Base schema for Task"""
    title: str = Field(..., min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: str = Field(default="pending", description="Task status (pending, in_progress, completed)")
    priority: str = Field(default="medium", description="Task priority (low, medium, high)")
    completed: bool = Field(default=False, description="Task completion status")


class TaskCreate(TaskBase):
    """Schema for creating a new task"""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task"""
    title: Optional[str] = Field(None, min_length=1, max_length=255, description="Task title")
    description: Optional[str] = Field(None, description="Task description")
    status: Optional[str] = Field(None, description="Task status (pending, in_progress, completed)")
    priority: Optional[str] = Field(None, description="Task priority (low, medium, high)")
    completed: Optional[bool] = Field(None, description="Task completion status")


class TaskResponse(TaskBase):
    """Schema for task response"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    """Schema for paginated task list response"""
    tasks: list[TaskResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    status_code: int


class MessageResponse(BaseModel):
    """Schema for simple message responses"""
    message: str

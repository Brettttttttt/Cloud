"""
Unit tests for Task CRUD operations
"""
import pytest
from fastapi import status


class TestTaskCreate:
    """Test task creation endpoint"""
    
    def test_create_task_success(self, client, sample_task_data):
        """Test successful task creation"""
        response = client.post("/api/v1/tasks", json=sample_task_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == sample_task_data["title"]
        assert data["description"] == sample_task_data["description"]
        assert data["status"] == sample_task_data["status"]
        assert data["priority"] == sample_task_data["priority"]
        assert data["completed"] == sample_task_data["completed"]
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data
    
    def test_create_task_minimal_data(self, client):
        """Test task creation with minimal required data"""
        minimal_data = {"title": "Minimal Task"}
        response = client.post("/api/v1/tasks", json=minimal_data)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["title"] == "Minimal Task"
        assert data["status"] == "pending"
        assert data["priority"] == "medium"
        assert data["completed"] is False
    
    def test_create_task_missing_title(self, client):
        """Test task creation without required title field"""
        invalid_data = {"description": "No title provided"}
        response = client.post("/api/v1/tasks", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        error_data = response.json()
        assert "error" in error_data
    
    def test_create_task_empty_title(self, client):
        """Test task creation with empty title"""
        invalid_data = {"title": ""}
        response = client.post("/api/v1/tasks", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestTaskRead:
    """Test task reading endpoints"""
    
    def test_get_all_tasks_empty(self, client):
        """Test getting tasks when database is empty"""
        response = client.get("/api/v1/tasks")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["tasks"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["total_pages"] == 0
    
    def test_get_all_tasks_with_data(self, client, create_sample_task):
        """Test getting all tasks"""
        # Create multiple tasks
        create_sample_task(title="Task 1")
        create_sample_task(title="Task 2")
        create_sample_task(title="Task 3")
        
        response = client.get("/api/v1/tasks")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["tasks"]) == 3
        assert data["total"] == 3
        assert data["page"] == 1
    
    def test_get_tasks_with_pagination(self, client, create_sample_task):
        """Test pagination"""
        # Create 15 tasks
        for i in range(15):
            create_sample_task(title=f"Task {i+1}")
        
        # Get first page
        response = client.get("/api/v1/tasks?page=1&page_size=5")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data["tasks"]) == 5
        assert data["total"] == 15
        assert data["total_pages"] == 3
        assert data["page"] == 1
        
        # Get second page
        response = client.get("/api/v1/tasks?page=2&page_size=5")
        data = response.json()
        assert len(data["tasks"]) == 5
        assert data["page"] == 2
    
    def test_get_tasks_filter_by_status(self, client, create_sample_task):
        """Test filtering tasks by status"""
        create_sample_task(status="pending")
        create_sample_task(status="completed")
        create_sample_task(status="pending")
        
        response = client.get("/api/v1/tasks?status=pending")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 2
        for task in data["tasks"]:
            assert task["status"] == "pending"
    
    def test_get_tasks_filter_by_priority(self, client, create_sample_task):
        """Test filtering tasks by priority"""
        create_sample_task(priority="high")
        create_sample_task(priority="low")
        create_sample_task(priority="high")
        
        response = client.get("/api/v1/tasks?priority=high")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 2
        for task in data["tasks"]:
            assert task["priority"] == "high"
    
    def test_get_single_task_success(self, client, create_sample_task):
        """Test getting a single task by ID"""
        task = create_sample_task(title="Single Task")
        
        response = client.get(f"/api/v1/tasks/{task.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == task.id
        assert data["title"] == "Single Task"
    
    def test_get_single_task_not_found(self, client):
        """Test getting a non-existent task"""
        response = client.get("/api/v1/tasks/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        error_data = response.json()
        assert "error" in error_data


class TestTaskUpdate:
    """Test task update endpoint"""
    
    def test_update_task_success(self, client, create_sample_task):
        """Test successful task update"""
        task = create_sample_task(title="Original Title")
        
        update_data = {
            "title": "Updated Title",
            "status": "completed",
            "completed": True
        }
        
        response = client.put(f"/api/v1/tasks/{task.id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Updated Title"
        assert data["status"] == "completed"
        assert data["completed"] is True
    
    def test_update_task_partial(self, client, create_sample_task):
        """Test partial task update"""
        task = create_sample_task(title="Original", priority="low")
        
        update_data = {"priority": "high"}
        
        response = client.put(f"/api/v1/tasks/{task.id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["title"] == "Original"  # Unchanged
        assert data["priority"] == "high"  # Updated
    
    def test_update_task_not_found(self, client):
        """Test updating a non-existent task"""
        update_data = {"title": "Updated"}
        response = client.put("/api/v1/tasks/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        error_data = response.json()
        assert "error" in error_data


class TestTaskDelete:
    """Test task deletion endpoint"""
    
    def test_delete_task_success(self, client, create_sample_task):
        """Test successful task deletion"""
        task = create_sample_task()
        
        response = client.delete(f"/api/v1/tasks/{task.id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        
        # Verify task is deleted
        get_response = client.get(f"/api/v1/tasks/{task.id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_delete_task_not_found(self, client):
        """Test deleting a non-existent task"""
        response = client.delete("/api/v1/tasks/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        error_data = response.json()
        assert "error" in error_data


class TestTaskStats:
    """Test task statistics endpoint"""
    
    def test_get_stats(self, client, create_sample_task):
        """Test getting task statistics"""
        create_sample_task(status="pending", completed=False)
        create_sample_task(status="in_progress", completed=False)
        create_sample_task(status="completed", completed=True)
        create_sample_task(status="completed", completed=True)
        
        response = client.get("/api/v1/tasks/stats/summary")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["total"] == 4
        assert data["completed"] == 2
        assert data["pending"] == 1
        assert data["in_progress"] == 1


class TestHealthEndpoints:
    """Test health check endpoints"""
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "app" in data
        assert "version" in data

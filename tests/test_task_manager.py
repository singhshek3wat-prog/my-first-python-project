import pytest
from datetime import datetime
from task_manager.models import Task, Priority, TaskStatus
from task_manager.storage import TaskStorage
import tempfile
from pathlib import Path


@pytest.fixture
def temp_storage():
    """Create a temporary storage for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        filepath = Path(tmpdir) / "tasks.json"
        yield TaskStorage(filepath=str(filepath))


class TestTaskModel:
    """Test the Task model."""

    def test_task_creation(self):
        """Test creating a task."""
        task = Task(
            title="Test Task",
            category="Work",
            priority=Priority.HIGH,
        )
        assert task.title == "Test Task"
        assert task.category == "Work"
        assert task.priority == Priority.HIGH
        assert task.status == TaskStatus.PENDING

    def test_mark_complete(self):
        """Test marking a task as complete."""
        task = Task(title="Test Task")
        assert task.status == TaskStatus.PENDING
        task.mark_complete()
        assert task.status == TaskStatus.COMPLETED
        assert task.completed_at is not None

    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task(
            title="Test Task",
            task_id=1,
            category="Work",
            priority=Priority.HIGH,
        )
        task_dict = task.to_dict()
        assert task_dict["id"] == 1
        assert task_dict["title"] == "Test Task"
        assert task_dict["priority"] == "high"
        assert task_dict["status"] == "pending"

    def test_task_from_dict(self):
        """Test creating a task from dictionary."""
        task_dict = {
            "id": 1,
            "title": "Test Task",
            "description": "Test Description",
            "category": "Work",
            "priority": "high",
            "status": "pending",
            "created_at": datetime.now().isoformat(),
            "completed_at": None,
        }
        task = Task.from_dict(task_dict)
        assert task.task_id == 1
        assert task.title == "Test Task"
        assert task.priority == Priority.HIGH


class TestTaskStorage:
    """Test the TaskStorage class."""

    def test_add_task(self, temp_storage):
        """Test adding a task."""
        task = Task(title="Test Task", category="Work")
        added_task = temp_storage.add_task(task)
        assert added_task.task_id == 1

    def test_get_all_tasks(self, temp_storage):
        """Test retrieving all tasks."""
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        temp_storage.add_task(task1)
        temp_storage.add_task(task2)
        tasks = temp_storage.get_all_tasks()
        assert len(tasks) == 2

    def test_get_task_by_id(self, temp_storage):
        """Test retrieving a specific task."""
        task = Task(title="Test Task")
        added = temp_storage.add_task(task)
        retrieved = temp_storage.get_task_by_id(added.task_id)
        assert retrieved is not None
        assert retrieved.title == "Test Task"

    def test_update_task(self, temp_storage):
        """Test updating a task."""
        task = Task(title="Original Title")
        added = temp_storage.add_task(task)
        added.title = "Updated Title"
        temp_storage.update_task(added)
        retrieved = temp_storage.get_task_by_id(added.task_id)
        assert retrieved.title == "Updated Title"

    def test_delete_task(self, temp_storage):
        """Test deleting a task."""
        task = Task(title="Task to Delete")
        added = temp_storage.add_task(task)
        temp_storage.delete_task(added.task_id)
        retrieved = temp_storage.get_task_by_id(added.task_id)
        assert retrieved is None

    def test_get_tasks_by_category(self, temp_storage):
        """Test filtering tasks by category."""
        task1 = Task(title="Work Task", category="Work")
        task2 = Task(title="Personal Task", category="Personal")
        temp_storage.add_task(task1)
        temp_storage.add_task(task2)
        work_tasks = temp_storage.get_tasks_by_category("Work")
        assert len(work_tasks) == 1
        assert work_tasks[0].title == "Work Task"

    def test_get_statistics(self, temp_storage):
        """Test getting statistics."""
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")
        added1 = temp_storage.add_task(task1)
        temp_storage.add_task(task2)
        added1.mark_complete()
        temp_storage.update_task(added1)
        stats = temp_storage.get_statistics()
        assert stats["total"] == 2
        assert stats["completed"] == 1
        assert stats["pending"] == 1

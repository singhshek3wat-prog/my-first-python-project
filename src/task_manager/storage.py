import json
import os
from pathlib import Path
from typing import List, Optional

from task_manager.models import Task, TaskStatus


class TaskStorage:
    """Handles persistence of tasks to JSON file."""

    def __init__(self, filepath: Optional[str] = None):
        if filepath is None:
            home = Path.home()
            filepath = home / ".task_manager" / "tasks.json"
        self.filepath = Path(filepath)
        self._ensure_storage_exists()

    def _ensure_storage_exists(self) -> None:
        """Create storage directory and file if they don't exist."""
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        if not self.filepath.exists():
            self.filepath.write_text(json.dumps({"tasks": [], "next_id": 1}))

    def _load_data(self) -> dict:
        """Load data from storage file."""
        try:
            return json.loads(self.filepath.read_text())
        except (json.JSONDecodeError, IOError):
            return {"tasks": [], "next_id": 1}

    def _save_data(self, data: dict) -> None:
        """Save data to storage file."""
        self.filepath.write_text(json.dumps(data, indent=2))

    def add_task(self, task: Task) -> Task:
        """Add a new task and return it with an assigned ID."""
        data = self._load_data()
        task.task_id = data["next_id"]
        data["tasks"].append(task.to_dict())
        data["next_id"] += 1
        self._save_data(data)
        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks that are not archived."""
        data = self._load_data()
        return [
            Task.from_dict(t)
            for t in data["tasks"]
            if Task.from_dict(t).status != TaskStatus.ARCHIVED
        ]

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Get a specific task by ID."""
        data = self._load_data()
        for task_data in data["tasks"]:
            if task_data["id"] == task_id:
                return Task.from_dict(task_data)
        return None

    def update_task(self, task: Task) -> bool:
        """Update an existing task."""
        data = self._load_data()
        for i, task_data in enumerate(data["tasks"]):
            if task_data["id"] == task.task_id:
                data["tasks"][i] = task.to_dict()
                self._save_data(data)
                return True
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID."""
        data = self._load_data()
        data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
        self._save_data(data)
        return True

    def get_tasks_by_category(self, category: str) -> List[Task]:
        """Get all tasks in a specific category."""
        return [
            t for t in self.get_all_tasks()
            if t.category.lower() == category.lower()
        ]

    def get_tasks_by_priority(self, priority_str: str) -> List[Task]:
        """Get all tasks with a specific priority."""
        return [
            t for t in self.get_all_tasks()
            if t.priority.value == priority_str.lower()
        ]

    def get_statistics(self) -> dict:
        """Get statistics about tasks."""
        all_tasks = self.get_all_tasks()
        completed = [t for t in all_tasks if t.status == TaskStatus.COMPLETED]
        overdue = [t for t in all_tasks if t.is_overdue()]

        return {
            "total": len(all_tasks),
            "completed": len(completed),
            "pending": len([t for t in all_tasks if t.status == TaskStatus.PENDING]),
            "overdue": len(overdue),
            "completion_rate": round(len(completed) / len(all_tasks) * 100, 1) if all_tasks else 0,
        }

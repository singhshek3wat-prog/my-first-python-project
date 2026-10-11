from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class Task:
    """Represents a single task."""
    title: str
    category: str = "Personal"
    priority: Priority = Priority.MEDIUM
    status: TaskStatus = TaskStatus.PENDING
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    task_id: Optional[int] = None

    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization."""
        return {
            "id": self.task_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }

    @staticmethod
    def from_dict(data: dict) -> 'Task':
        """Create a Task from a dictionary."""
        return Task(
            task_id=data["id"],
            title=data["title"],
            description=data.get("description"),
            category=data.get("category", "Personal"),
            priority=Priority(data.get("priority", "medium")),
            status=TaskStatus(data.get("status", "pending")),
            created_at=datetime.fromisoformat(data["created_at"]),
            completed_at=datetime.fromisoformat(data["completed_at"]) if data.get("completed_at") else None,
        )

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.status = TaskStatus.COMPLETED
        self.completed_at = datetime.now()

    def is_overdue(self) -> bool:
        """Check if task is pending and was created more than a week ago."""
        if self.status != TaskStatus.PENDING:
            return False
        days_old = (datetime.now() - self.created_at).days
        return days_old > 7

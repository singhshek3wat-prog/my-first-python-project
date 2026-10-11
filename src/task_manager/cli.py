import argparse
import sys
from task_manager.models import Priority, Task
from task_manager.storage import TaskStorage


class TaskManagerCLI:
    """Main CLI interface for task manager."""

    def __init__(self):
        self.storage = TaskStorage()

    def add(self, args) -> None:
        """Add a new task."""
        task = Task(
            title=args.title,
            category=args.category,
            priority=Priority(args.priority.lower()),
            description=args.description,
        )
        added_task = self.storage.add_task(task)
        print(f"✅ Task added with ID {added_task.task_id}: {added_task.title}")

    def list_tasks(self, args) -> None:
        """List tasks with optional filters."""
        if args.category:
            tasks = self.storage.get_tasks_by_category(args.category)
        elif args.priority:
            tasks = self.storage.get_tasks_by_priority(args.priority.lower())
        else:
            tasks = self.storage.get_all_tasks()

        if not tasks:
            print("No tasks found.")
            return

        print(f"\n{'ID':<4} {'Status':<12} {'Priority':<8} {'Category':<12} {'Title':<30}")
        print("-" * 70)
        for task in tasks:
            status_icon = "✅" if task.status.value == "completed" else "⏳"
            print(
                f"{task.task_id:<4} {status_icon} {task.status.value:<10} "
                f"{task.priority.value:<8} {task.category:<12} {task.title:<30}"
            )
        print()

    def complete(self, args) -> None:
        """Mark a task as complete."""
        task = self.storage.get_task_by_id(args.task_id)
        if not task:
            print(f"❌ Task {args.task_id} not found.")
            return
        task.mark_complete()
        self.storage.update_task(task)
        print(f"✅ Task {args.task_id} marked as complete!")

    def delete(self, args) -> None:
        """Delete a task."""
        if self.storage.delete_task(args.task_id):
            print(f"🗑️  Task {args.task_id} deleted.")
        else:
            print(f"❌ Task {args.task_id} not found.")

    def update(self, args) -> None:
        """Update a task."""
        task = self.storage.get_task_by_id(args.task_id)
        if not task:
            print(f"❌ Task {args.task_id} not found.")
            return

        if args.title:
            task.title = args.title
        if args.priority:
            task.priority = Priority(args.priority.lower())
        if args.category:
            task.category = args.category
        if args.description:
            task.description = args.description

        self.storage.update_task(task)
        print(f"✅ Task {args.task_id} updated.")

    def stats(self, args) -> None:
        """Show task statistics."""
        stats = self.storage.get_statistics()
        print(f"\n📊 Task Statistics:")
        print(f"   Total tasks: {stats['total']}")
        print(f"   Completed: {stats['completed']}")
        print(f"   Pending: {stats['pending']}")
        print(f"   Overdue: {stats['overdue']}")
        print(f"   Completion rate: {stats['completion_rate']}%\n")


def main(argv=None) -> int:
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="Task Manager - A professional task management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  task-manager add "Complete project" --priority high --category Work
  task-manager list --category Work
  task-manager complete 1
  task-manager delete 1
  task-manager stats
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument(
        "--description", "-d", help="Task description", default=None
    )
    add_parser.add_argument(
        "--category", "-c", help="Task category", default="Personal"
    )
    add_parser.add_argument(
        "--priority",
        "-p",
        choices=["low", "medium", "high"],
        default="medium",
        help="Task priority",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.add_argument(
        "--category", "-c", help="Filter by category", default=None
    )
    list_parser.add_argument(
        "--priority",
        "-p",
        choices=["low", "medium", "high"],
        help="Filter by priority",
        default=None,
    )

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
    complete_parser.add_argument("task_id", type=int, help="Task ID")

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", type=int, help="Task ID")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update a task")
    update_parser.add_argument("task_id", type=int, help="Task ID")
    update_parser.add_argument("--title", "-t", help="New title", default=None)
    update_parser.add_argument(
        "--description", "-d", help="New description", default=None
    )
    update_parser.add_argument(
        "--category", "-c", help="New category", default=None
    )
    update_parser.add_argument(
        "--priority",
        "-p",
        choices=["low", "medium", "high"],
        help="New priority",
        default=None,
    )

    # Stats command
    subparsers.add_parser("stats", help="Show task statistics")

    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    cli = TaskManagerCLI()
    command_map = {
        "add": cli.add,
        "list": cli.list_tasks,
        "complete": cli.complete,
        "delete": cli.delete,
        "update": cli.update,
        "stats": cli.stats,
    }

    try:
        command_map[args.command](args)
        return 0
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

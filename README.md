# Task Manager CLI

A professional command-line task management application built with Python. Demonstrates best practices in software design, testing, and CLI development.

## Features

- ✅ **Create, read, update, and delete tasks**
- 📝 **Task persistence** using JSON storage
- 🏷️ **Task categories** (Work, Personal, Shopping, etc.)
- 🔴 **Priority levels** (Low, Medium, High)
- ✔️ **Mark tasks as complete**
- 📊 **View all tasks** with filtering options
- 🗑️ **Archive completed tasks**

## Quick Start

```bash
pip install -e .
```

## Usage

### Add a task
```bash
task-manager add "Complete project proposal" --priority high --category Work
```

### List tasks
```bash
task-manager list
task-manager list --category Work
task-manager list --priority high
```

### Mark task as complete
```bash
task-manager complete 1
```

### Update a task
```bash
task-manager update 1 --title "Updated title" --priority medium
```

### Delete a task
```bash
task-manager delete 1
```

### View statistics
```bash
task-manager stats
```

## Project Structure

```
src/task_manager/
├── __init__.py          # Package metadata
├── __main__.py          # CLI entry point
├── cli.py              # Command-line interface
├── models.py           # Task data model
├── storage.py          # File persistence layer
└── commands/
    ├── __init__.py
    ├── add.py          # Add command
    ├── list.py         # List command
    ├── complete.py     # Complete command
    ├── delete.py       # Delete command
    ├── update.py       # Update command
    └── stats.py        # Statistics command
```

## Design Patterns Used

- **Command Pattern**: Encapsulates each CLI command as a class
- **Repository Pattern**: Abstracts data storage from business logic
- **Factory Pattern**: Creates task objects with validation
- **Single Responsibility Principle**: Each module has one clear purpose

## Testing

```bash
pip install pytest pytest-cov
pytest
pytest --cov=src/task_manager  # Coverage report
```

## Technologies

- Python 3.9+
- Click (optional: for enhanced CLI)
- pytest for testing
- JSON for data persistence

## Why This Project?

This project demonstrates:
- ✅ Clean code architecture
- ✅ Comprehensive testing
- ✅ Error handling
- ✅ User-friendly CLI design
- ✅ Data persistence
- ✅ Professional documentation


"""
Task model and repository.
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict, Any


class Task:
    """Task entity class representing a single task."""

    def __init__(self, title: str, description: str = "", priority: int = 3,
                 due_date: Optional[str] = None, completed: bool = False,
                 task_id: Optional[int] = None, created_at: Optional[str] = None,
                 updated_at: Optional[str] = None):
        self.id = task_id
        self.title = title
        self.description = description
        self.priority = max(1, min(5, priority))  # Ensure between 1-5
        self.due_date = due_date
        self.completed = completed
        self.created_at = created_at or datetime.now().isoformat()
        self.updated_at = updated_at or datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date,
            'completed': self.completed,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }


class TaskRepository(ABC):
    """Abstract base class for task repository."""

    @abstractmethod
    def get_all(self) -> List[Task]:
        pass

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    def create(self, task: Task) -> Task:
        pass

    @abstractmethod
    def update(self, task_id: int, task_data: Dict[str, Any]) -> Optional[Task]:
        pass

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        pass

    @abstractmethod
    def mark_completed(self, task_id: int, completed: bool) -> Optional[Task]:
        pass


class SQLiteTaskRepository(TaskRepository):
    """SQLite implementation of TaskRepository."""

    def __init__(self, db_connection):
        self.db = db_connection

    def get_all(self) -> List[Task]:
        """Get all tasks."""
        with self.db() as conn:
            cursor = conn.execute("""
                SELECT * FROM tasks 
                ORDER BY 
                    CASE WHEN completed = 1 THEN 1 ELSE 0 END,
                    priority ASC,
                    due_date ASC
            """)
            tasks = []
            for row in cursor:
                tasks.append(Task(
                    task_id=row['id'],
                    title=row['title'],
                    description=row['description'],
                    priority=row['priority'],
                    due_date=row['due_date'],
                    completed=bool(row['completed']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                ))
            return tasks

    def get_by_id(self, task_id: int) -> Optional[Task]:
        """Get task by ID."""
        with self.db() as conn:
            cursor = conn.execute(
                "SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            if row:
                return Task(
                    task_id=row['id'],
                    title=row['title'],
                    description=row['description'],
                    priority=row['priority'],
                    due_date=row['due_date'],
                    completed=bool(row['completed']),
                    created_at=row['created_at'],
                    updated_at=row['updated_at']
                )
            return None

    def create(self, task: Task) -> Task:
        """Create a new task."""
        with self.db() as conn:
            cursor = conn.execute("""
                INSERT INTO tasks (title, description, priority, due_date, completed)
                VALUES (?, ?, ?, ?, ?)
            """, (task.title, task.description, task.priority,
                  task.due_date, task.completed))
            task.id = cursor.lastrowid
            conn.commit()
            return task

    def update(self, task_id: int, task_data: Dict[str, Any]) -> Optional[Task]:
        """Update an existing task."""
        update_data = {k: v for k, v in task_data.items()
                       if v is not None and k != 'id'}

        if not update_data:
            return None

        update_data['updated_at'] = datetime.now().isoformat()

        set_clause = ", ".join(f"{key} = ?" for key in update_data.keys())
        values = list(update_data.values())
        values.append(task_id)

        with self.db() as conn:
            conn.execute(f"""
                UPDATE tasks 
                SET {set_clause}
                WHERE id = ?
            """, values)
            conn.commit()

            return self.get_by_id(task_id)

    def delete(self, task_id: int) -> bool:
        """Delete a task."""
        with self.db() as conn:
            cursor = conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    def mark_completed(self, task_id: int, completed: bool) -> Optional[Task]:
        """Mark task as completed or not."""
        with self.db() as conn:
            conn.execute("""
                UPDATE tasks 
                SET completed = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (completed, task_id))
            conn.commit()
            return self.get_by_id(task_id)

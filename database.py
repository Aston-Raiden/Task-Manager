"""
Database connection and initialization module.
"""
import sqlite3
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    """Manages database connections with context manager support."""

    def __init__(self, db_path="tasks.db"):
        self.db_path = db_path

    def __enter__(self):
        """Open database connection."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Return rows as dictionaries
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Close database connection."""
        if exc_type:
            logger.error(f"Database error: {exc_val}")
        self.conn.close()


def init_database():
    """
    Initialize the database with required tables.
    """
    schema = """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        priority INTEGER NOT NULL DEFAULT 3 CHECK(priority BETWEEN 1 AND 5),
        due_date DATE,
        completed BOOLEAN NOT NULL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE INDEX IF NOT EXISTS idx_tasks_priority ON tasks(priority);
    CREATE INDEX IF NOT EXISTS idx_tasks_due_date ON tasks(due_date);
    CREATE INDEX IF NOT EXISTS idx_tasks_completed ON tasks(completed);
    """

    try:
        with DatabaseConnection() as conn:
            conn.executescript(schema)
            logger.info("Database initialized successfully")
    except sqlite3.Error as e:
        logger.error(f"Database initialization failed: {e}")
        raise


def get_db():
    """Factory function to get database connection."""
    return DatabaseConnection()

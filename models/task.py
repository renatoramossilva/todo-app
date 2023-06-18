"""
This module provides functionality for managing tasks in a SQLite database.
"""
import sqlite3

# Query to create table
CREATE_TABLE = "CREATE TABLE IF NOT EXISTS tasks (  \
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,      \
    title text TEXT,                                \
    description text TEXT NOT NULL,                 \
    due_date date NOT NULL,                         \
    completed BOOLEAN NOT NULL                      \
)"

DATABASE = "tasks.db"


class TaskModel:
    """Represents a task object."""

    def __init__(
        self,
        task_id: int = None,
        title: str = None,
        description: str = None,
        due_date: str = "",
        completed: str = "False",
    ):  # pylint: disable=too-many-arguments
        if task_id:
            self.task_id = task_id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.completed = completed

    def to_json(self) -> dict:
        """Convert the TaskModel object to a JSON-formatted dictionary."""
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "due_date": self.due_date,
            "completed": self.completed,
        }

    def to_list(self) -> list:
        """Convert the TaskModel object to a list."""
        return [
            self.title,
            self.description,
            self.due_date,
            self.completed,
            self.task_id,
        ]

    def save(self) -> None:
        """
        Save the task to the database.
        """
        conn, cursor = connect_db()
        cursor.execute(
            "INSERT INTO tasks (title, description, due_date, completed) VALUES (?, ?, ?, ?)",
            (self.title, self.description, self.due_date, "False"),
        )
        self.task_id = cursor.lastrowid
        self.completed = "False"
        conn.commit()
        conn.close()

    def delete(self) -> None:
        """
        Delete the task from the database.
        """
        conn, cursor = connect_db()
        cursor.execute("DELETE FROM tasks WHERE task_id=?", (self.task_id,))
        conn.commit()
        conn.close()

    def update(self) -> None:
        """
        Update the task details in the database.
        """
        conn, cursor = connect_db()
        query = "UPDATE tasks SET title=?, description=?, due_date=?, completed=? WHERE task_id=?"

        cursor.execute(query, self.to_list())
        conn.commit()
        conn.close()


def create_table() -> None:
    """
    Create the 'tasks' table in the SQLite database.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE)
    conn.commit()
    conn.close()


def connect_db() -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    """
    Establish a connection to the SQLite database.

    This function connects to the database, creating a cursor,
    and returns both the connection and cursor objects.

    :returns:
        - The connection object representing the database connection.
        - The cursor object for executing SQL statements on the database.
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    return conn, cursor


def get_task_by_id(task_id: str) -> TaskModel:
    """
    Retrieve a task from the database by its ID.

    This function queries the database for a task with the specified ID
    and returns it as a TaskModel object.

    :param task_id: The ID of the task to retrieve.

    :returns: The TaskModel object representing the retrieved task,
        or None if no task is found.
    """
    conn, cursor = connect_db()
    query = "SELECT task_id, title, description, due_date, completed FROM tasks WHERE task_id=?"
    cursor.execute(query, (task_id,))
    row = TaskModel(*cursor.fetchone())
    conn.close()
    return row or None


def get_all_tasks() -> TaskModel:
    """
    Retrieve all tasks from the database.

    This function queries the database and returns all tasks as a list of tuples
        representing each row in the tasks table.

    :return: A list of tuples representing the retrieved tasks,
        or None if no tasks are found.
    """
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    return rows or None


def get_uncompleted_tasks() -> TaskModel:
    """
    Retrieve all uncompleted tasks from the database.

    This function queries the database and returns a list of TaskModel objects
        representing the uncompleted tasks.

    :returns: A list of TaskModel objects representing the uncompleted tasks,
        or None if no uncompleted tasks are found.
    """
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM tasks WHERE completed='False'")
    rows = [TaskModel(*task) for task in cursor.fetchall()]
    conn.close()
    return rows or None

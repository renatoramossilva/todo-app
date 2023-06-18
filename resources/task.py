"""
This module contains resources and models for managing tasks through a REST API.
"""
from flask_restful import Resource, reqparse
from models.task import TaskModel, get_task_by_id, get_all_tasks


class TaskBase(Resource):
    """
    Base class for task resources.
    """

    args = reqparse.RequestParser()
    args.add_argument("title")
    args.add_argument("description")
    args.add_argument("due_date")
    args.add_argument("completed")


class Tasks(TaskBase):
    """
    Resource for managing tasks.
    """

    def get(self) -> dict:  # pylint: disable=no-self-use
        """
        Get all tasks.
        """
        all_tasks = []
        for task in get_all_tasks():
            all_tasks.append(task)

        return {"tasks": all_tasks}

    def post(self) -> dict:
        """
        Create a new task.
        """
        data = self.args.parse_args()
        new_task = TaskModel(**data)
        new_task.save()

        return new_task.to_json()


class Task(TaskBase):
    """
    Resource for managing a single task.
    """

    def get(self, task_id: str) -> dict:  # pylint: disable=no-self-use
        """
        Get details of a given task.
        """
        return {"tasks": [task for task in get_all_tasks() if str(task[0]) == task_id]}

    def put(self, task_id: str) -> tuple[dict, int]:
        """
        Update details of a given task.
        """
        data = self.args.parse_args()
        task = TaskModel(task_id, **data)

        if get_task_by_id(task_id):
            task.update()
            return task.to_json(), 200

        task.save()
        return task.to_json(), 201

    def delete(self, task_id: str) -> dict:  # pylint: disable=no-self-use
        """
        Delete a specific task.
        """
        task = get_task_by_id(task_id)
        if task:
            del_task = TaskModel(*[task])
            del_task.delete()
            return {"message": "Task deleted"}
        return {"message": "Task not found"}

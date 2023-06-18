"""
This module implements a Flask application for managing tasks.

It provides the following routes:
- GET /: Displays the index page with the list of uncompleted tasks.
- POST /process: Processes form data to create or update a task.
- POST /complete_task/<task_id>: Marks a task as completed.
- POST /delete_task/<task_id>: Deletes a task.
- GET /edit_task/<task_id>: Displays the form to edit a specific task.

The module also defines the following resources:
- /tasks/: Provides a RESTful API endpoint for listing tasks and creating new tasks.
- /tasks/<task_id>: Provides a RESTful API endpoint for
    retrieving, updating, and deleting a specific task.
"""
import flask
from flask_restful import Api
from resources.task import Task, Tasks
from models.task import TaskModel, get_uncompleted_tasks, get_task_by_id, create_table

app = flask.Flask(__name__)
api = Api(app)

api.add_resource(Tasks, "/tasks/")
api.add_resource(Task, "/tasks/<string:task_id>")


@app.route("/")
def index() -> str:
    """
    Render the index page.

    :returns: A rendered HTML template for the index page, with a list of uncompleted tasks.
    """
    return flask.render_template("index.html", tasks=get_uncompleted_tasks())


@app.route("/process", methods=["POST"])
def process_data() -> flask.wrappers.Response:
    """
    Process form data to create or update a task.

    Retrieves form data for task_id, title, description, and due_date from a POST request.
    Creates a TaskModel object with the retrieved data.
    If task_id is provided, updates the corresponding task.
    Otherwise, saves the new task.
    Finally, redirects the user to the index page.

    :returns: A redirect response to the index page.

    """
    _task_id = flask.request.form.get("task_id", None)
    _title = flask.request.form.get("title", None)
    _description = flask.request.form.get("description", None)
    _due_date = flask.request.form.get("due_date", None)
    task = TaskModel(task_id=_task_id, title=_title, description=_description, due_date=_due_date)
    if _task_id:
        task.update()
    else:
        task.save()
    return flask.redirect(flask.url_for("index"))


@app.route("/complete_task/<string:task_id>", methods=["POST"])
def complete_task(task_id: str) -> flask.wrappers.Response:
    """
    Mark a task as completed.

    Retrieves the task with the given task_id from the database.
    If the task exists, sets its completed attribute to "True" and updates the task in the database.
    Finally, redirects the user to the index page.

    :param task_id: The ID of the task to be marked as completed.

    :returns: A redirect response to the index page.
    """
    task = get_task_by_id(task_id)
    if task:
        task.completed = "True"
        task.update()
    print(type(flask.redirect(flask.url_for("index"))))
    return flask.redirect(flask.url_for("index"))


@app.route("/delete_task/<string:task_id>", methods=["POST"])
def delete_task(task_id: str) -> flask.wrappers.Response:
    """
    Delete a task.

    Retrieves the task with the given task_id from the database.
    If the task exists, deletes it from the database.
    Finally, redirects the user to the index page.

    :param task_id: The ID of the task to be deleted.

    :returns: A redirect response to the index page.

    """
    task = get_task_by_id(task_id)
    if task:
        task.delete()
    return flask.redirect(flask.url_for("index"))


@app.route("/edit_task/<string:task_id>", methods=["GET"])
def edit_task(task_id: str) -> str:
    """
    Display the form to edit a specific task.

    Retrieves the task with the given task_id from the database.
    Renders the index.html template with the edit_task flag set to True and the task details.

    :param task_id: The ID of the task to be edited.

    :returns: The rendered HTML template.

    """
    task = get_task_by_id(task_id)
    return flask.render_template(
        "index.html",
        edit_task=True,
        task_id=task.task_id,
        title=task.title,
        description=task.description,
        due_date=task.due_date,
    )


if __name__ == "__main__":
    create_table()
    app.run()

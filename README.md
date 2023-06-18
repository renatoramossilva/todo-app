Software Developer test - Numentech
====================

## Database
- [SQLite](https://www.sqlite.org/)

# Steps to Run the ToDo App

## Create/Activate the Virtual Environment

`python3 -m venv ~/venv_todoapp`
`source ~/venv_todoapp/bin/activate`

## Install the Requirements

`pip install -r requirements.txt`

## Execute The ToDo App

`python3 app.py`

## Interface

To access the management interface of the tasks, click [here](127.0.0.1:5000)

Once the page is loaded, you will see two blocks:

The first one consists of three fields (title, description and due_date) that allow the user to add/edit tasks, and the submit button, to save them in the database.

The second block shows the tasks marked as uncompleted.


## Tests

Open the terminal and run `sqlite3 tasks.db` to procedure with the tests

```
> sqlite3 tasks.db
SQLite version 3.39.5 2022-10-14 20:58:05
Enter ".help" for usage hints.
sqlite>
```

Confirm that database is empty:

`SELECT * FROM tasks;`

```
sqlite> SELECT * FROM tasks;
sqlite> |
```

### Add task

Go back to the interface and add a new task:

e.g.
    Title: My task 1
    Description: This is my task 1
    Due Date: 06/19/2023

After adding a new task, you will be able to see the task information in the ToDo List block.

To confirm that the task is in the database, please run:

```
sqlite> SELECT * FROM tasks;
1|My task 1|This is my task 1|2023-06-19|False
```

### Edit task

Click on Edit to load the task information. Now you can edit the title, description, and due date for the chosen task.

e.g.
    Title: My task 1 - Edited
    Description: This is my task 1!
    Due Date: 06/20/2023

After editing the desired fields, click on Save.

To confirm that the task was updated successfully, please run:

```
sqlite> SELECT * FROM tasks;
1|My task 1 - Edited|This is my task 1!|2023-06-20|False
```

### Mark as completed

When a new task is added to the database the field `complete` is saved as `False` (uncompleted task) by default, (See `save` function on `models/task.py`) and The ToDo List block only shows these tasks.

The button `Mark as completed` updates the field `complete` to `True`, so the tasks is no longer visible from the perspective of The Todo List block, but it is still in the database.


Checking if the task was updated:

```
sqlite> SELECT * FROM tasks;
1|My task 1 - Edited|This is my task 1!|2023-06-20|True
```

### Delete task

Add a new task:

e.g.
    Title: My task 2
    Description: This is my task 2
    Due Date: 02/06/2023

```
sqlite> SELECT * FROM tasks;
1|My task 1 - Edited|This is my task 1!|2023-06-20|True
2|My task 2|This is my task 2|2023-02-06|False
```

Clicking on `Delete` button the task will be deleted from the database.

```
sqlite> SELECT * FROM tasks;
1|My task 1 - Edited|This is my task 1!|2023-06-20|True
```

# Extras

## Code Formatter

The python code was auto format using black.

```
black .

reformatted ~/resources/task.py

All done! ✨ 🍰 ✨
1 file reformatted, 4 files left unchanged.

```

## Code Analyser

The code was parsed by pylint.

```
pylint **/*.py


--------------------------------------------------------------------
Your code has been rated at 10.00/10 (previous run: 10.00/10, +0.00)
```



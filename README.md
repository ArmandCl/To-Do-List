# Toudou 
## Designed by Armand CLOUZEAU Info2 B

Toudou is a task management application that can be used in two ways: through the Command-Line Interface (CLI) or a Graphical User Interface (GUI) developed with Flask.
```bash
How to install the project :
$ python -m pdm install           # install project dependencies
$ python -m pdm run toudou        # run the project
$ python -m pdm run flask --app toudou.views --debug run or $ pdm start #start the Flask application then go to 127.0.0.1:5000

Commands:
    create a task
    update a task
    delete a task
    Export the database into a csv file
        - the csv file will be placed in the "db" directory
    Import a database with a csv file
```
## How the Project is Made

For this project, there are three main files: `models.py`, `services.py`, and `views.py`. I've implemented a Model-View-Controller (MVC) architecture.

### `models.py`

In `models.py`, I've defined the structure for handling data related to tasks. The file starts by importing necessary modules and defining constants. Then, it declares a table `todos_table` using SQLAlchemy's `Table` class, specifying columns such as `id`, `task`, `complete`, and `due`. 

Next, a `Todo` data class is defined using Python's `dataclass` decorator to represent a single task. This class includes attributes like `id`, `task`, `complete`, and `due`.

Following this, various functions are defined to interact with the database. For example, `init_db()` initializes the database, `create_todo()` creates a new task, `get_todo()` retrieves a task by its ID, and so on. These functions utilize SQLAlchemy's functionalities for database operations.

### `services.py`

In `services.py`, functionalities related to importing and exporting CSV files are handled. Let's delve into the provided code:

#### Exporting to CSV (`export_to_csv()`)

The `export_to_csv()` function is responsible for exporting tasks to a CSV file. It first retrieves all tasks using the `get_all_todos()` function from `models.py`. Then, it specifies the filename for the CSV file and writes the task data into it. Each task is represented as a row in the CSV file, with columns such as `id`, `task`, `complete`, and `due`. The `due` date is formatted as an ISO string using `isoformat()` if it exists. Finally, the function returns 0 upon successful export, or 1 if there are no tasks to export.

#### Importing from CSV (`import_from_csv(csv_file)`)

The `import_from_csv(csv_file)` function handles the importing of tasks from a CSV file. It uses the pandas library to read the CSV file. Then, it iterates over each row of the DataFrame obtained from the CSV file. For each row, it extracts the task, due date, and completeness status. The due date is converted to a Python `datetime` object. Subsequently, it calls the `create_todo()` function from `models.py` to create a new task with the extracted information. The function returns different error codes depending on various scenarios, such as an empty CSV file, parsing errors, or other unspecified errors.

This module efficiently manages the import and export operations, enhancing the project's data handling capabilities.

### `views.py`

In `views.py`, the user interface and interaction functionalities are implemented using Flask. Let's explore the provided code:

#### Command-line Interface (CLI) Commands

The `click` library is utilized to define command-line interface commands for various operations. These commands include:

- `init_db()`: Initializes the database.
- `create(task, due)`: Creates a new task with the provided task description and due date.
- `get(id)`: Retrieves a task by its ID.
- `get_all(as_csv)`: Retrieves all tasks, optionally exporting them as CSV if the `as_csv` flag is set.
- `import_csv(csv_file)`: Imports tasks from a CSV file.
- `update(id, complete, task, due)`: Updates a task with the provided information.
- `delete(id)`: Deletes a task by its ID.
- `affiche_table()`: Displays tables in the database.

#### Web User Interface (Web UI)

`Flask` is used to create a web application with multiple routes for user interaction. Key functionalities include:

- Rendering HTML templates for user interfaces.
- Handling form submissions for inserting, updating, and deleting tasks.
- Implementing authentication and authorization using HTTP Basic Authentication.
- Defining forms for inserting, updating, and deleting tasks.
- Handling errors with appropriate error pages and redirects.
- Providing routes for exporting and importing tasks as CSV files.
- Implementing role-based access control for administrative views.

This architecture separates concerns effectively, with `models.py` managing data, `services.py` handling file operations, and `views.py` managing user interactions.


```bash
List of all libraries installed in PDM get with `pdm list`:
╭───────────────────┬──────────────┬──────────────────────────────────────────╮
│ name              │ version      │ location                                 │
├───────────────────┼──────────────┼──────────────────────────────────────────┤
│ blinker           │ 1.7.0        │                                          │
│ click             │ 8.1.7        │                                          │
│ colorama          │ 0.4.6        │                                          │
│ Flask             │ 3.0.3        │                                          │
│ Flask-HTTPAuth    │ 4.8.0        │                                          │
│ Flask-WTF         │ 1.2.1        │                                          │
│ greenlet          │ 3.0.3        │                                          │
│ itsdangerous      │ 2.1.2        │                                          │
│ Jinja2            │ 3.1.3        │                                          │
│ MarkupSafe        │ 2.1.5        │                                          │
│ numpy             │ 1.26.4       │                                          │
│ pandas            │ 2.2.1        │                                          │
│ python-dateutil   │ 2.9.0.post0  │                                          │
│ pytz              │ 2024.1       │                                          │
│ six               │ 1.16.0       │                                          │
│ SQLAlchemy        │ 2.0.29       │                                          │
│ Toudou            │ 0.1+editable │ -e C:\Users\armandc\Documents\To-Do-List │
│ typing_extensions │ 4.11.0       │                                          │
│ tzdata            │ 2024.1       │                                          │
│ Werkzeug          │ 3.0.2        │                                          │
│ WTForms           │ 3.1.2        │                                          │
╰───────────────────┴──────────────┴──────────────────────────────────────────╯

```

Course & examples : [https://kathode.neocities.org](https://kathode.neocities.org)

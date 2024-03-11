import click
import uuid

from datetime import datetime

import toudou.models as models
import toudou.services as services
from flask import render_template, Flask, request,Response

app = Flask(__name__)

@click.group()
def cli():
    pass


@cli.command()
def init_db():
    models.init_db()


@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(), default=None, help="Due date of the task.")
def create(task: str, due: datetime):
    models.create_todo(task, due=due)


@cli.command()
@click.option("--id", required=True, type=click.UUID, help="Todo's id.")
def get(id: uuid.UUID):
    click.echo(models.get_todo(id))


@cli.command()
@click.option("--as-csv", is_flag=True, help="Ouput a CSV string.")
def get_all(as_csv: bool):
    if as_csv:
        click.echo(services.export_to_csv())
    else:
        click.echo(models.get_all_todos())


@cli.command()
@click.argument("csv_file", type=click.File("r"))
def import_csv(csv_file):
    services.import_from_csv(csv_file)


@cli.command()
@click.option("--id", required=True, type=click.UUID, help="Todo's id.")
@click.option("-c", "--complete", required=True, type=click.BOOL, help="Todo is done or not.")
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
@click.option("-d", "--due", type=click.DateTime(), default=None, help="Due date of the task.")
def update(id: uuid.UUID, complete: bool, task: str, due: datetime):
    models.update_todo(id, task, complete, due)


@cli.command()
@click.option("--id", required=True, type=click.UUID, help="Todo's id.")
def delete(id: uuid.UUID):
    models.delete_todo(id)

@cli.command()
def affiche_table():
    models.display_tables()

@app.route('/')
def accueil():
    models.init_db()
    tasks = models.get_all_todos()
    return render_template("index.html", tasks=tasks)

@app.route('/insert', methods=['POST'])
def insert_task():
    message = ""
    if request.method == 'POST':
        task = request.form['Task']
        due = datetime.strptime(request.form['date'], "%Y-%m-%d") if request.form['date'] else None

        if models.create_todo(task, due=due):
            message = "Task created successfully"
        else:
            message = "Failed to create task"

    tasks = models.get_all_todos()
    return render_template("index.html", tasks=tasks, message=message)

@app.route('/update', methods=['POST'])
def update_task():
    message = ""
    if request.method == 'POST':
        id_update = uuid.UUID(request.form['id'])
        todo_to_update = models.get_todo(id_update)

        new_task = todo_to_update.task if request.form['Task'] == "" else request.form['Task']
        new_complete = request.form.get('Complete', 'False') == 'on'
        new_due = datetime.strptime(request.form['Date'], "%Y-%m-%d") if 'Date' in request.form and request.form.get('Date') else todo_to_update.due

        models.update_todo(id_update, new_task, new_complete, new_due)
        message = "Task updated successfully"

    tasks = models.get_all_todos()
    return render_template("index.html", tasks=tasks, message=message)

@app.route('/delete', methods=['POST'])
def delete_task():
    message = ""
    if request.method == 'POST':
        id_delete = request.form['id']
        models.delete_todo(id_delete)
        message = "Task deleted successfully"

    tasks = models.get_all_todos()
    return render_template("index.html", tasks=tasks, message=message)

@app.route('/exportcsv', methods=['POST'])
def export_csv():

    tasks = models.get_all_todos()
    export = services.export_to_csv()
    if export == 0:
        message = "Export successful. Data written to /db/db.csv"
    else:
        message = "No data to export !"
    return render_template("index.html", tasks=tasks, message=message)

@app.route('/importcsv', methods=['POST'])
def import_csv():
    # Get the list of tasks before import
    tasks_before_import = models.get_all_todos()

    # Check if a CSV file has been provided in the request
    if 'csv_file' not in request.files:
        message = "No CSV file provided."
        return render_template("index.html", tasks=tasks_before_import, message=message)

    csv_file = request.files['csv_file']

    # Check if the file has a proper name and extension
    if csv_file.filename == '' or not csv_file.filename.endswith('.csv'):
        message = "Invalid CSV file."
        return render_template("index.html", tasks=tasks_before_import, message=message)

    # Call the import function with the CSV file
    import_result = services.import_from_csv(csv_file)

    # Get the list of tasks after import
    tasks_after_import = models.get_all_todos()

    if import_result == 0:
        message = "Import successful."
    elif import_result == 1:
        message = "No data imported. The CSV file is empty."
    elif import_result == 2:
        message = "Error reading the CSV file."
    else:
        message = "An unspecified error occurred during import. (It's probably due to the date !)"

    # Use the list of tasks before import if an error occurred
    tasks = tasks_after_import if import_result == 0 else tasks_before_import

    return render_template("index.html", tasks=tasks, message=message)
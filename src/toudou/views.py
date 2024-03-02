import click
import uuid

from datetime import datetime

import toudou.models as models
import toudou.services as services
from flask import render_template, Flask, request

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
        click.echo(services.export_to_csv().getvalue())
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
# Flask route
@app.route('/', methods=['GET', 'POST'])
def accueil():
    models.init_db()
    message = ""
    if request.method == 'POST':
        if 'add_task' in request.form:
            task = request.form['Task']
            if request.form['date']:
                due = datetime.strptime(request.form['date'], "%Y-%m-%d")
            else:
                due = None

            if models.create_todo(task, due=due):
                message = "Task created successfully"
            else:
                message = "Failed to create task"

        elif 'delete_task' in request.form:
            id_delete = request.form['id']
            models.delete_todo(id_delete)
            message = "Task deleted successfully"

    # Collect tasks after either adding or deleting
    tasks = models.get_all_todos()

    return render_template("index.html", tasks=tasks, message=message)



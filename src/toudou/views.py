import logging

import click
import uuid

from datetime import datetime

import toudou.models as models
import toudou.services as services
from flask import render_template, Flask, request,Response, Blueprint, flash, redirect, url_for, abort
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired

from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from werkzeug.security import generate_password_hash,check_password_hash
from flask_pydantic_spec import FlaskPydanticSpec, Request
from pydantic import BaseModel, Field, constr

import os

secret_key = "secret"

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

@cli.command()
@click.option("-u", "--username",required=True, prompt="Your username")
@click.option("-p", "--password",required=True, prompt="Your password")
@click.option("--role", default="member")
def create_user(username: str, password: str, role:str):
    models.create_user(username,password,role)

@cli.command()
@click.option("--id", required=True, type=click.UUID, help="User's id.")
def get_user(id: uuid.UUID):
    models.get_user(id)

web_ui =Blueprint("web_ui",__name__, url_prefix="/")
api=Blueprint("api_ui",__name__, url_prefix="/api")
auth= HTTPBasicAuth()
auth_token = HTTPTokenAuth(scheme='Bearer')
api_spec = FlaskPydanticSpec('flask')

users = {
    "armand": generate_password_hash("armand"),
    "admin": generate_password_hash("admin")
}

roles = {
    "member": ["armand"],
    "admin": ["admin"]
}
class InsertTodoForm(FlaskForm):
    insert_task = StringField('Task', validators=[DataRequired()])
    insert_date = StringField('Date')
    submit = SubmitField('Submit')

class UpdateTodoForm(FlaskForm):
    ID_update = StringField('ID_update', validators=[DataRequired()], render_kw={'type': 'hidden'})
    update_task = StringField('Task')
    complete = BooleanField('Complete')
    update_date = StringField('Date')
    submit = SubmitField('Submit')

class DeleteTodoForm(FlaskForm):
    ID_delete = StringField('ID_delete', validators=[DataRequired()], render_kw={'type': 'hidden'})
    submit = SubmitField('Submit')

class Profile(BaseModel):
    username: str
    password: str
    role: str

tokens = {
    "secret-token-1": "armand",
    "secret-token-2": "admin"
}

def create_app():
    app = Flask(__name__)
    api_spec.register(app)
    from toudou.views import web_ui
    app.register_blueprint(web_ui)
    app.register_blueprint(api)
    app.secret_key = secret_key

    return app


@web_ui.route('/')
@auth.login_required()
def accueil():
    models.init_db()

    insert_form = InsertTodoForm()
    update_form = UpdateTodoForm()
    delete_form = DeleteTodoForm()

    tasks = models.get_all_todos()
    return render_template("index.html", tasks=tasks, insert_form=insert_form, update_form=update_form, delete_form=delete_form)


@web_ui.route('/insert', methods=["GET", "POST"])
@auth.login_required(role="admin")
def insert_task():
    insert_form = InsertTodoForm()
    update_form = UpdateTodoForm()
    delete_form = DeleteTodoForm()
    message = ""

    if insert_form.validate_on_submit():
        task = insert_form.insert_task.data
        due = datetime.strptime(insert_form.insert_date.data, "%Y-%m-%d") if insert_form.insert_date.data else None

        if models.create_todo(task, due=due):
            message = "Task created successfully"
            insert_form = InsertTodoForm()
        else:
            message = "Failed to create task"

    tasks = models.get_all_todos()
    return render_template("index.html", tasks=tasks, insert_form=insert_form, update_form=update_form, delete_form=delete_form)



@web_ui.route('/update', methods=["GET", "POST"])
@auth.login_required(role="admin")
def update_task():
    message = ""
    insert_form = InsertTodoForm()
    update_form = UpdateTodoForm()
    delete_form = DeleteTodoForm()

    if update_form.validate_on_submit():
        id_update = uuid.UUID(update_form.ID_update.data)
        todo_to_update = models.get_todo(id_update)

        new_task = todo_to_update.task if update_form.update_task.data == "" else update_form.update_task.data
        new_complete = update_form.complete.data
        new_due = datetime.strptime(update_form.update_date.data, "%Y-%m-%d") if update_form.update_date.data else todo_to_update.due

        models.update_todo(id_update, new_task, new_complete, new_due)
        message = "Task updated successfully"
        update_form = UpdateTodoForm()
    else :
        message = "Failed to update the task"

    tasks = models.get_all_todos()
    return render_template("index.html", tasks=tasks, message=message, insert_form=insert_form, update_form=update_form, delete_form=delete_form)

@web_ui.route('/delete', methods=["GET", "POST"])
@auth.login_required(role="admin")
def delete_task():
    message = ""
    update_form = UpdateTodoForm()
    insert_form = InsertTodoForm()
    delete_form = DeleteTodoForm()

    if delete_form.validate_on_submit():
        id_delete = delete_form.ID_delete.data
        models.delete_todo(id_delete)
        message = "Task deleted successfully"
    else:
        message = "Failed to delete the task"
    tasks = models.get_all_todos()
    return render_template("index.html", tasks=tasks, message=message, insert_form=insert_form,
                           update_form=update_form, delete_form=delete_form)


@web_ui.route('/delete_all', methods=['POST'])
@auth.login_required(role="admin")
def delete_all():
    message = ""
    update_form = UpdateTodoForm()
    insert_form = InsertTodoForm()
    delete_form = DeleteTodoForm()
    if request.method == 'POST':
        models.delete_all()
        message = "All the tasks have been delete successfully"

    tasks = models.get_all_todos()
    return render_template("index.html", tasks=tasks, message=message, insert_form=insert_form,update_form=update_form, delete_form=delete_form)


@web_ui.route('/exportcsv', methods=["GET", "POST"])
@auth.login_required()
def export_csv():
    tasks = models.get_all_todos()
    update_form = UpdateTodoForm()
    insert_form = InsertTodoForm()
    delete_form = DeleteTodoForm()
    export = services.export_to_csv()
    if export == 0:
        message = "Export successful. Data written to /db/db.csv"
    else:
        message = "No data to export !"
    return render_template("index.html", tasks=tasks, message=message, insert_form=insert_form,update_form=update_form, delete_form=delete_form)

@web_ui.route('/importcsv', methods=["GET", "POST"])
@auth.login_required(role="admin")
def import_csv():
    # Get the list of tasks before import
    tasks_before_import = models.get_all_todos()
    update_form = UpdateTodoForm()
    insert_form = InsertTodoForm()
    delete_form = DeleteTodoForm()

    # Check if a CSV file has been provided in the request
    if 'csv_file' not in request.files:
        message = "No CSV file provided."
        return render_template("index.html", tasks=tasks_before_import, message=message, insert_form=insert_form,update_form=update_form, delete_form= delete_form)

    csv_file = request.files['csv_file']

    # Check if the file has a proper name and extension
    if csv_file.filename == '' or not csv_file.filename.endswith('.csv'):
        message = "Invalid CSV file."
        return render_template("index.html", tasks=tasks_before_import, message=message, insert_form=insert_form,update_form=update_form, delete_form=delete_form)

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

    return render_template("index.html", tasks=tasks, message=message, insert_form=insert_form,update_form=update_form, delete_form=delete_form)

@web_ui.errorhandler(500)
def handle_internal_error(error):
    logging.exception(error)
    return redirect(url_for(".accueil"))

@web_ui.errorhandler(404)
def handle_internal_error(error):
    logging.exception(error)
    return redirect(url_for(".accueil"))

@web_ui.errorhandler(403)
def handle_internal_error(error):
    logging.exception(error)
    return redirect(url_for(".accueil"))

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@auth.get_user_roles
def get_user_roles(user):
    if user in roles["admin"]:
        return ["admin"]
    elif user in roles["member"]:
        return ["member"]
    else:
        return []


@web_ui.route("/admin")
@auth.login_required(role="admin")
def admin_view():
    if auth.current_user() in roles["admin"]:
        return f"Hello {auth.current_user()}, you are an admin!"
    else:
        abort(403)



@auth_token.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

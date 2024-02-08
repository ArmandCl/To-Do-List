import datetime
import pickle
import click
import uuid
import pandas as pd
from dataclasses import dataclass


@dataclass
class Todo:
    id: uuid.UUID
    task: str
    description: str
    status: bool
    deadline: datetime

@click.group()
def cli():
    pass


@cli.command()
@click.option("-t", "--task", prompt="Your task", help="The task to remember.")
def display(task: str):
    todo = Todo(uuid.uuid4(), task)
    click.echo(todo)

@cli.command()
@click.option("-t","--task",prompt="Task to add",help="The task you want to add.")
@click.option("-desc","--description",prompt="Description",help="The description of your task.")
@click.option("-d","--deadline",type=click.DateTime(formats=["%Y-%m-%d"]),default = None ,help="The deadline of your task.")
def add(task: str,description: str,deadline: datetime):

    #ask the user if we wants to add a deadline
    ask_deadline = click.prompt("Do you want to add a deadline? (y/n)", default="n", type=str)

    if ask_deadline.lower() == "y":
        deadline = click.prompt("Enter the deadline (YYYY-MM-DD):", type=click.DateTime(formats=["%Y-%m-%d"]))

    status = False
    todo = Todo(uuid.uuid4(),task,description, status, deadline)
    with open('data/todo.p','ab') as f:
        pickle.dump(todo,f)
    click.echo("Task add succesfuly")


@cli.command()
def show():
     with open('data/todo.p', 'rb') as f:
        while True:
            todo = pickle.load(f)
            click.echo(f"ID: {todo.id}, Task: {todo.task}, Description: {todo.description}, Status: {todo.status}, Deadline: {todo.deadline}\n")


def load_data():
    data = []
    try:
        with open('data/todo.p', 'rb') as f:
            while True:
                try:
                    todo = pickle.load(f)
                    data.append(todo)
                except EOFError:
                    break
    except FileNotFoundError:
        click.echo("File not found. No data loaded.")
    except Exception as e:
        click.echo(f"Error during the loading of the data: {e}")
    return data



@cli.command()
@click.option("--id", prompt="Task to search", help="The task you want to search.")
def search(id: str):
    try:
        search_id = uuid.UUID(id)
    except ValueError:
        click.echo("Invalid UUID format")
        return

    data = load_data()
    found_task = None

    for todo in data:
        if todo.id == search_id:
            found_task = todo
            click.echo(todo)
            return found_task

    if found_task is None:
        click.echo("Task not found")

@cli.command()
@click.option("--id", prompt="Task to modify", help="The task you want to modify.")
def modify(id :str):

    todos = load_data()

    # ask the user if he wants to change the task name
    ask_name = click.prompt("Do you want to change the task name? (y/n)", default="n", type=str)
    if ask_name.lower() == "y":
        new_name = click.prompt("Enter the new name:", type=str)

    # ask the user if he wants to change the task description
    ask_description = click.prompt("Do you want to change the task description ? (y/n)", default="n", type=str)
    if ask_description.lower() == "y":
        new_description = click.prompt("Enter the new description:", type=str)

    # ask the user if he wants to change the task status
    ask_status = click.prompt("Do you want to change the task description ? (y/n)", default="n", type=str)
    if ask_status.lower() == "y":
        new_status = click.prompt("Enter the new status:", type=bool)

    #ask the user if he wants to change the deadline
    ask_deadline = click.prompt("Do you want to change the deadline? (y/n)", default="n", type=str)
    if ask_deadline.lower() == "y":
        new_deadline = click.prompt("Enter the new deadline (YYYY-MM-DD):", type=click.DateTime(formats=["%Y-%m-%d"]))

    for todo in todos:
        if todo.id == id:
            todo.task = new_name
            todo.description = new_description
            todo.status = new_status
            todo.deadline = new_deadline

    with open('data/todo.p', 'wb') as f:
        for todo in todos:
            pickle.dump(todo, f)
    click.echo("Task well modify")
@cli.command()
@click.option("--id", prompt="Task to delete", help="The task you want to delete.")
def delete(id: str):
    """
    Deletes a specific task from the todo list.

    We can't directly delete a task in the pickle file, so we are creating a new list without the task chosen by the user,
    and we write the new list above the old pickle file.

    Parameters:
    - id (str): The task to be deleted.
    """
    new_todolist = [todo for todo in load_data() if todo.id != id]

    with open('data/todo.p', 'wb') as f:
        for todo in new_todolist:
            pickle.dump(todo, f)

    click.echo("Task deleted successfully.")

@cli.command()
def exportcsv():
    """
    to export the pickle's file into a csv file, we are going to use Pandas
    """
    data = load_data()

    if not data:
        click.echo("No data to export.")
        return

    df = pd.DataFrame([vars(todo) for todo in data])
    df.to_csv('data/todo.csv', index=False)
    click.echo("Data exported to 'data/todo.csv' successfully.")

@cli.command()
@click.option("--csv-file", prompt="CSV file path", help="Path to the CSV file to import.")
@click.option("--pickle-file", prompt="Pickle file path", help="Path to save the converted pickle file.")
def importcsv(csv_file: str, pickle_file: str):
    """
    Import data from a CSV file, convert, and save as a pickle file.
    """
    try:
        # Read data from CSV file into a DataFrame
        df = pd.read_csv(csv_file)

        # Convert DataFrame to list of Todo objects
        data = [Todo(**row) for index, row in df.iterrows()]

        # Save data as a pickle file
        with open(pickle_file, 'wb') as f:
            pickle.dump(data, f)

        click.echo(f"Data imported and saved as '{pickle_file}' successfully.")
    except FileNotFoundError:
        click.echo(f"CSV file '{csv_file}' not found. No data imported.")
    except Exception as e:
        click.echo(f"Error during import and pickle conversion: {e}")



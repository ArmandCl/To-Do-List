import datetime
import pickle
import click
import uuid

from dataclasses import dataclass


@dataclass
class Todo:
    id: uuid.UUID
    task: str
    description : str
    status : bool
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








#faire la commande modify
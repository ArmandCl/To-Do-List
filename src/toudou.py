import datetime
import pickle
import click
import uuid

from dataclasses import dataclass


@dataclass
class Todo:
    id: uuid.UUID
    task: str
    delete: str
    deadline: datetime = None

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
@click.option("-d","--deadline",prompt="Deadline",help="The deadline of your task.")
def add(task: str,deadline: datetime):
    todo = Todo(uuid.uuid4(),task,deadline)
    with open('data/todo.p','ab') as f:
        pickle.dump(todo,f)
    click.echo("Task add succesfuly")


@cli.command()
def show():
     with open('data/todo.p', 'rb') as f:
        while True:
            todo = pickle.load(f)
            if hasattr(todo, 'deadline'):
                click.echo(f"ID: {todo.id}, Task: {todo.task}, Deadline: {todo.deadline}\n")
            else:
                click.echo(f"ID: {todo.id}, Task: {todo.task}")


#faire la methode delete
@cli.command()
@click.option("-d","--delete",prompt="Task to delete",help="The task you want to delete.")
def delete(delete: str):
    with open('data/todo.p', 'rb') as f:
        # faire avec un for
        donnees = pickle.load(f)
        if delete in donnees:
            del donnees[delete]
            print(f"Donnée '{delete}' supprimée avec succès.")
        else:
            print(f"Donnée '{delete}' non trouvée.")






#faire la commande modify
import datetime
import pickle
import click
import uuid

from dataclasses import dataclass


@dataclass
class Todo:
    id: uuid.UUID
    task: str
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
import pickle
import click
import uuid

from dataclasses import dataclass


@dataclass
class Todo:
    id: uuid.UUID
    task: str
    j_fin: int
    m_fin: int
    y_fin: int


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
@click.option("--j_fin",prompt="Day of end",help="The day you want your task to end.")
@click.option("--m_fin",prompt="Mounth of end",help="The mounth you want your task to end.")
@click.option("--y_fin",prompt="Year of end",help="The year you want your task to end.")
def add(task:str,j_fin:int, m_fin:int, y_fin:int):
    todo = Todo(uuid.uuid4(),task,j_fin,m_fin,y_fin)
    with open('data/todo.p','ab') as f:
        pickle.dump(todo,f)
    click.echo("Task add succesfuly")


@cli.command()
def show():
     with open('data/todo.p', 'rb') as f:
        while True:
            todo = pickle.load(f)
            if hasattr(todo, 'j_fin'):
                click.echo(f"ID: {todo.id}, Task: {todo.task}, Deadline: {todo.j_fin}/{todo.m_fin}/{todo.y_fin}\n")
            else:
                click.echo(f"ID: {todo.id}, Task: {todo.task}")
import os
import pickle
import uuid

from dataclasses import dataclass
from datetime import datetime
from typing import List
from toudou import config

from sqlalchemy import create_engine, MetaData, Table, Column, Uuid, Integer, String, Boolean, DateTime, engine, Engine, \
    inspect, select, insert, bindparam,delete

from werkzeug.security import generate_password_hash


TODO_FOLDER = config["TOUDOU_FOLDER"]
metadata = MetaData()
engine = create_engine(config["DATABASE_URL"], echo=config["DEBUG"])
todos_table = Table(
        "todos",
        metadata,
        Column("id", Uuid, primary_key=True, default=uuid.uuid4),
        Column("task", String, nullable=False),
        Column("complete", Boolean, nullable=False),
        Column("due", DateTime, nullable=True)
    )

users_table = Table(
    "users",
    metadata,
    Column("id_user", Uuid, primary_key=True, default=uuid.uuid4),
    Column("username", String, nullable=False),
    Column("password", String, nullable=False),
    Column("role", String, nullable=False)
)

@dataclass
class Todo:
    id: uuid.UUID
    task: str
    complete: bool
    due: datetime | None

@dataclass
class User:
    id_user : uuid.UUID
    username: str
    password: str
    role: str

def init_db() -> None:
    global metadata, engine, todos_table, users_table
    os.makedirs(TODO_FOLDER, exist_ok=True)

    metadata.create_all(engine)


def display_tables() -> None:
    global metadata, engine
    print("Tables dans la base de données:")
    for table_name in inspect(engine).get_table_names():
        todos_table = Table(table_name, metadata, autoload_with=engine)
        print(f"Nom de la table: {table_name}")
        print(f"Colonnes de la table: {todos_table.c.keys()}")


def read_from_file(filename: str) -> Todo:
    with open(os.path.join(TODO_FOLDER, filename), "rb") as f:
        return pickle.load(f)


def write_to_file(todo: Todo, filename: str) -> None:
    with open(os.path.join(TODO_FOLDER, filename), "wb") as f:
        pickle.dump(todo, f)


def create_todo(
        task: str,
        complete: bool = False,
        due: datetime | None = None
) -> int:
    global engine, metadata, todos_table

    stmt = todos_table.insert().values(
        task=task,
        complete=complete,
        due=due
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)
        return result.rowcount > 0


def get_todo(id: uuid.UUID) -> Todo:
    global engine, metadata, todos_table

    # Sélectionne toutes les colonnes de la table todos où l'ID correspond
    stmt = select(todos_table).where(todos_table.c.id == id)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        todo_row = result.fetchone()  # Récupère la première ligne correspondante

    if todo_row is not None:
        # Construit un objet Todo à partir des valeurs de la ligne récupérée
        todo = Todo(
            id=todo_row[0],
            task=todo_row[1],
            complete=todo_row[2],
            due=todo_row[3]
        )
        return todo
    else:
        raise ValueError(f"No todo found with ID {id}")

def charge_todos():
    global engine, metadata, todos_table

    # Sélectionne toutes les colonnes de la table todos
    stmt = select(todos_table)

    with engine.begin() as conn:
        result = conn.execute(stmt)
        todos = []
        for row in result.fetchall():
            todo = Todo(
                id=row[0],  # L'ID est à l'indice 0
                task=row[1],  # La tâche est à l'indice 1
                complete=row[2],  # L'état complet est à l'indice 2
                due=row[3]  # La date d'échéance est à l'indice 3
            )
            todos.append(todo)
    return todos
def get_all_todos() -> List[Todo]:
    todos = charge_todos()
    # Affiche les tâches récupérées
    if todos:
        print("Todos:")
        for todo in todos:
            print(f"ID: {todo.id}, Task: {todo.task}, Complete: {todo.complete}, Due: {todo.due}")
    else:
        print("No todos found")

    return todos

def update_todo(
    id: uuid.UUID,
    task: str,
    complete: bool,
    due: datetime | None
) -> None:
    global engine, metadata, todos_table

    update_stmt = todos_table.update().where(todos_table.c.id == id).values(
        task=task,
        complete=complete,
        due=due
    )

    with engine.begin() as conn:
        result = conn.execute(update_stmt)
        if result.rowcount > 0:
            print("Update successfully ")
        else:
            print(f"No todo found with ID {id}")




def delete_todo(id_str: str) -> None:
    global engine, metadata, todos_table

    try:
        # Convert the string ID to a UUID object
        id = uuid.UUID(id_str)
    except ValueError as e:
        print(f"Error converting {id_str} to UUID: {e}")
        return

    delete_stmt = todos_table.delete().where(todos_table.c.id == id)

    with engine.begin() as conn:
        result = conn.execute(delete_stmt)
        if result.rowcount > 0:
            print("Delete successfully ")
        else:
            print(f"No todo found with ID {id}")

def delete_all():
    global engine, todos_table

    delete_stmt = todos_table.delete()

    with engine.begin() as conn:
        result = conn.execute(delete_stmt)
        if result.rowcount > 0:
            print("Delete successfully ")
        else:
            print("No todos found to delete")


def create_user(username: str, password: str, role:str) -> int:
    global engine, metadata, users_table

    hashed_password = generate_password_hash(password)

    stmt = users_table.insert().values(
        id=uuid.uuid4(),
        username=username,
        password=hashed_password,
        role=role
    )

    with engine.begin() as conn:
        result = conn.execute(stmt)
        return result.rowcount > 0

def get_user(id : Uuid) -> User:
    global engine, metadata, users_table

    # Sélectionne toutes les colonnes de la table user où l'ID correspond
    stmt = select(users_table).where(users_table.c.id_user == id)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        user_row = result.fetchone()  # Récupère la première ligne correspondante

    if user_row is not None:
        # Construit un objet User à partir des valeurs de la ligne récupérée
        user = User(
            id_user=user_row[0],
            username=user_row[1],
            password=user_row[2],
            role=user_row[3]
        )
        return user
    else:
        raise ValueError(f"No user found with ID {id}")

def get_user_by_username(username: str) -> User | None:
    global engine, metadata, users_table

    # Sélectionne toutes les colonnes de la table user où le nom d'utilisateur correspond
    stmt = select(users_table).where(users_table.c.username == username)

    with engine.connect() as conn:
        result = conn.execute(stmt)
        user_row = result.fetchone()  # Récupère la première ligne correspondante

    if user_row is not None:
        # Construit un objet User à partir des valeurs de la ligne récupérée
        user = User(
            id_user=user_row[0],
            username=user_row[1],
            password=user_row[2],
            role=user_row[3]
        )
        return user
    else:
        return None

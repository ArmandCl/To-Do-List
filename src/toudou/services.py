import csv
import dataclasses
import io

from datetime import datetime

import pandas as pd
from toudou.models import create_todo, get_all_todos, Todo
from toudou import config


def export_to_csv() -> int:
    # Utilise la méthode get_all_todos pour récupérer les tâches
    todos = get_all_todos()
    filename = config["FILE_NAME_CSV"]
    if todos:
        # Écrire les données dans un fichier CSV
        csv_columns = ["id", "task", "complete", "due"]
        with open(filename, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_columns)
            writer.writeheader()
            for todo in todos:
                writer.writerow({
                    "id": str(todo.id),
                    "task": todo.task,
                    "complete": str(todo.complete),
                    "due": todo.due.isoformat() if todo.due else None
                })
        return 0 #succes
    else:
        return 1 #error


def import_from_csv(csv_file) -> int:
    try:
        # Lecture du fichier CSV avec pandas
        df = pd.read_csv(csv_file)

        for index, row in df.iterrows():
            task = row['task']
            due_temp = row['due']
            due = pd.to_datetime(due_temp, errors='coerce').to_pydatetime() if pd.notna(due_temp) else None
            complete = bool(row['complete'])

            if due:
                create_todo(task, due=due, complete=complete)
            else:
                create_todo(task, complete=complete)

        return 0  # Succès
    except pd.errors.EmptyDataError:
        return 1  # Le fichier CSV est vide
    except pd.errors.ParserError:
        return 2  # Erreur lors de la lecture du fichier CSV
    except Exception as e:
        return 3  # Autre erreur non spécifiée
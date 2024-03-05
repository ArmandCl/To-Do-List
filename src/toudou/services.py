import csv
import dataclasses
import io

from datetime import datetime

from toudou.models import create_todo, get_all_todos, Todo


def export_to_csv() -> None:
    # Utilise la méthode get_all_todos pour récupérer les tâches
    todos = get_all_todos()
    filename = "./db/db.csv"
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


def import_from_csv(csv_file: io.StringIO) -> None:
    csv_reader = csv.DictReader(
        csv_file,
        fieldnames=[f.name for f in dataclasses.fields(Todo)]
    )
    for row in csv_reader:
        create_todo(
            task=row["task"],
            due=datetime.fromisoformat(row["due"]) if row["due"] else None,
            complete=row["complete"] == "True"
        )

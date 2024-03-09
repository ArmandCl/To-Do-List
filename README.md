# Toudou 
## Designed by Armand CLOUZEAU Info2 B

Toudou is a task management application that can be used in two ways: through the Command-Line Interface (CLI) or a Graphical User Interface (GUI) developed with Flask.
```bash
How to install the project :
$ python -m pdm install           # install project dependencies
$ python -m pdm run toudou        # run the project
$ python -m pdm run flask --app toudou.views --debug run  #start the Flask application then go to 127.0.0.1:5000

Commands:
    create a task
    update a task
    delete a task
    Export the database into a csv file
    Import a database with a csv file
    
List of all libraries installed in PDM:
╭───────────────────┬──────────────┬──────────────────────────────────────────────╮
│ name              │ version      │ location                                     │
├───────────────────┼──────────────┼──────────────────────────────────────────────┤
│ blinker           │ 1.7.0        │                                              │
│ click             │ 8.1.7        │                                              │
│ colorama          │ 0.4.6        │                                              │
│ Flask             │ 3.0.2        │                                              │
│ greenlet          │ 3.0.3        │                                              │
│ itsdangerous      │ 2.1.2        │                                              │
│ Jinja2            │ 3.1.3        │                                              │
│ MarkupSafe        │ 2.1.5        │                                              │
│ numpy             │ 1.26.4       │                                              │
│ pandas            │ 2.2.1        │                                              │
│ python-dateutil   │ 2.9.0.post0  │                                              │
│ pytz              │ 2024.1       │                                              │
│ six               │ 1.16.0       │                                              │
│ SQLAlchemy        │ 2.0.28       │                                              │
│ Toudou            │ 0.1+editable │ -e C:\Users\Arman\PycharmProjects\To-Do-List │
│ typing_extensions │ 4.10.0       │                                              │
│ tzdata            │ 2024.1       │                                              │
│ Werkzeug          │ 3.0.1        │                                              │
╰───────────────────┴──────────────┴──────────────────────────────────────────────╯

```

Course & examples : [https://kathode.neocities.org](https://kathode.neocities.org)

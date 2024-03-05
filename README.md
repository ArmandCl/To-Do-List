# Toudou 
## Designed by Armand CLOUZEAU Info2 B

Toudou is a task management application that can be used in two ways: through the Command-Line Interface (CLI) or a Graphical User Interface (GUI) developed with Flask.
```bash
How to install the project :
$ python -m pip install pdm       # Python Dependency Manager is recommended
$ python -m pdm install           # install project dependencies
$ python -m pdm run toudou        # run the project
$ python -m pdm run flask --app toudou.views --debug run  #start the Flask application. Go to 127.0.0.1:5000
Usage: toudou [OPTIONS] COMMAND [ARGS]...

Options:
    --help  Show this message and exit.

Commands:
    create a task
    update a task
    delete a task
    Export the database into a csv file
    Import a database with a csv file
```

Course & examples : [https://kathode.neocities.org](https://kathode.neocities.org)

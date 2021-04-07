# cs411G7

## Flask directory structure
Everything is organized according to https://flask.palletsprojects.com/en/1.1.x/tutorial/layout/
The current app folder is called *playlist_maker* but we can change this in the future when we come
up with a better name.

## Setting up a development environment
Make sure that all API keys and sensitive info are stored in `instance/config.py`

While developing the application, it can be helpful to setup a python virtual environment for package management.

### You can install virtualenv with:

*On macOS and Linux:*

`python3 -m pip install --user virtualenv`

*On Windows:*

`py -m pip install --user virtualenv`

### Next, just create a venv with:

*On macOS and Linux:*

`python3 -m venv env`

*On Windows:*

`py -m venv env`

### Then you can activate the venv with:

*On macOS and Linux:*

`source env/bin/activate`

*On Windows:*

`.\env\Scripts\activate`

Now when you use python, it should be from the venv source, so your environment will be isolated to the project and you won't mess with your native environment + you can easily test things with a clean slate.

Once you are done with the venv, you can leave it by running `deactivate`

## Installing the flask app for development

After you have activated your venv, run

`python setup.py install develop`

By adding `develop`, when a change is added you won't need to reinstall every time you make a change, since a symbolic link is created to the project directory instead of copying everything to the python site-packages.

## Running the flask app

Now, just run the following to start up the flask app 

(instructions from https://flask.palletsprojects.com/en/1.1.x/tutorial/factory/#run-the-application)

*On macOS and Linux*
```
$ export FLASK_APP=playlist_maker
$ export FLASK_ENV=development
$ flask run
```

*On Windows CMD*
```
> set FLASK_APP=playlist_maker
> set FLASK_ENV=development
> flask run
```

*On Windows PowerShell*
```
> $env:FLASK_APP = "playlist_maker"
> $env:FLASK_ENV = "development"
> flask run
```

## Running tests
Install all test requirements with `pip install -e .[test]` and run all tests with `pytest`

Check `pytest --help` for more options

## Extra notes / structure clarifications

The file named `playlist_maker/__init__.py` contains the functions of the app. (we can split more complex functionality into blueprints later, see https://flask.palletsprojects.com/en/1.1.x/blueprints/)

The `playlist_maker/templates` folder contains the front-end HTML.

Before running the prototype example, you need to *manually* generate an auth token and insert it into the code where indicated. We will change this in the future.

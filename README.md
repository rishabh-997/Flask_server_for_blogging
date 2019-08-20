# Flask_server_for_blogging
This repo has server codes for creating a blogging web application for which tech slack being used is Python, PyCharm, HTML.

# Important commands

**Date** : 19/08/2019

- python3 -m venv myvenv
- source myvenv/bin/activate

- pip install flask
- pip install python-dotenv
- flask run

- first create a view.py file, then add template for it, then update routes.py accordingly to do calculations

- pip install flask-sqlachemy ---  SQLAlchemy package, which is an Object Relational Mapper or ORM. ORMs allow applications to manage a database using high-level entities such as classes, objects and methods instead of tables and SQL. The job of the ORM is to translate the high-level operations into database commands.
- pip install flask-migrate   ---  a database migration framework for SQLAlchemy. Working with database migrations adds a bit of work to get a database started, but that is a small price to pay for a robust way to make changes to your database in the future.

- update config file, create models.py to contain database columns
- make changes in __init__.py file
- flask db init
- flask db migrate
- flask db upgrade
- flask db downgrade to revert previous changes

- from werkzeug.security import generate_password_hash, check_password_hash

- pip install flask-login 
- Instantiate LoginManager in __init.py__ file
- Add UserMaxim function in models
- add user_loader function in functions.
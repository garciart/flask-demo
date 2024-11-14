# Tracker v08a

This is a demo of a Flask application that incorporates a database.

-----

## Usage

> **NOTE** - Remember to activate your Python virtual environment before running:
>
> - `source venv/bin/activate` (Linux)
> - `venv/Scripts/activate` (Windows)

Runs the Flask application using HTML files found in the `templates` directory:

- python -B -m flask --app tracker_08a run
- python -B -m flask --app "tracker_08a:create_app('development', True)" run

> **NOTE** - Enclose options in quotation marks when using special characters.

-----

## Notes

The purpose of the Tracker application is to track course assignments and, in order to do that, it needs a database.

Short version:

We are using SQLite, a relational database that is built into the Python Standard Library.
We are using SQLAlchemy, an open-source Python library that provides an SQL toolkit and an Object Relational Mapper for database interactions.
There are several ways for Flask to interact with a database: the Raw SQL Method, the SQL with Classes Method, the SQLAlchemy Imperative (Classical) Method, and the SQLAlchemy Declarative Method
Using the SQLAlchemy Declarative Method results in smaller and cleaner code and easy integration with object-oriented programming.

To get started, install the SQLAlchemy library:

```sh
python -m pip install Flask-SQLAlchemy
python -m pip freeze > requirements.txt
```

Long version:

First, there was the Raw SQL Method:

```python
"""Raw SQL Method
"""

import sqlite3

# Step 1: Connect to the SQLite database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Step 2: Create the User table
cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    user_id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL UNIQUE,
    user_email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
)
''')

# Step 3: Add a user
cursor.execute('''
INSERT INTO user (user_name, user_email, password_hash)
VALUES (?, ?, ?)
''', ('john_doe', 'john@example.com', 'hashed_password'))

# Step 4: Commit the changes
conn.commit()

# Step 5: Fetch all users
cursor.execute('SELECT * FROM user')
users = cursor.fetchall()
print(users)

# Step 6: Close the connection
conn.close()
```

Then, there was the SQL with Classes Method:

```python
"""SQL and Classes method
"""

import sqlite3

class User:
    def __init__(self, user_id=None, user_name=None, user_email=None, password_hash=None):
        self.user_id = user_id
        self.user_name = user_name
        self.user_email = user_email
        self.password_hash = password_hash

    @classmethod
    def create_table(cls, cursor):
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY,
            user_name TEXT NOT NULL UNIQUE,
            user_email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
        ''')

    @classmethod
    def insert(cls, cursor, user_name, user_email, password_hash):
        cursor.execute('''
        INSERT INTO user (user_name, user_email, password_hash)
        VALUES (?, ?, ?)
        ''', (user_name, user_email, password_hash))

    @classmethod
    def get_all(cls, cursor):
        cursor.execute('SELECT * FROM user')
        return cursor.fetchall()

# Step 1: Connect to the SQLite database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Step 2: Create the User table
User.create_table(cursor)

# Step 3: Add a user
User.insert(cursor, 'john_doe', 'john@example.com', 'hashed_password')

# Step 4: Commit the changes
conn.commit()

# Step 5: Fetch all users
users = User.get_all(cursor)
print(users)

# Step 6: Close the connection
conn.close()
```

Next, there was SQLAlchemy and Object-Relational Mapping (ORM) with imperative mapping:

```python
"""Imperative or Classical Mapping
"""

from sqlalchemy import Table, Column, Integer, String, create_engine
from sqlalchemy.orm import registry, sessionmaker

# Initialize the registry and define the table
mapper_registry = registry()

user_table = Table(
    "user",
    mapper_registry.metadata,
    Column("user_id", Integer, primary_key=True),
    Column("user_name", String(64), nullable=False, unique=True),
    Column("user_email", String(320), nullable=False, unique=True),
    Column("password_hash", String(128), nullable=False),
)

# Define a class (no need to add any fields here since we're using the Table-based mapping)
class User:
    pass

# Map the class to the table
mapper_registry.map_imperatively(User, user_table)

# Step 1: Connect to the SQLite database and create the session
engine = create_engine('sqlite:///your_database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Step 2: Create the table in the database (if not exists)
mapper_registry.metadata.create_all(engine)  # Creates the table if it doesn't exist

# Step 3: Add a new user
new_user = {
    'user_name': 'john_doe',
    'user_email': 'john@example.com',
    'password_hash': 'hashed_password',
}

# Insert the new user into the table
session.execute(user_table.insert().values(new_user))

# Commit the changes
session.commit()

# Step 4: Fetch all users
result = session.execute(user_table.select())
users = result.fetchall()  # Fetch all rows

# Check if we found any users and print them
if users:
    for user in users:
        print(f'User found: {user}')  # Each `user` is a Row object, print as is or extract columns
else:
    print('No users found')

# Step 5: Close the session
session.close()
```

Now, we use SQLAlchemy and ORM with declarative mapping:

```python
"""Declarative Mapping
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Step 1: Define the model
class User(DeclarativeBase):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    user_email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

# Step 2: Set up the database engine and session
engine = create_engine('sqlite:///your_database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Step 3: Create the tables (if they don't exist)
Base.metadata.create_all(engine)

# Step 4: Insert a new user into the database
new_user = User(user_name='john_doe', user_email='john@example.com', password_hash='hashed_password')
session.add(new_user)  # Add the user object to the session
session.commit()  # Commit the transaction to persist the user

# Step 5: Query all users from the database
users = session.query(User).all()  # Fetch all users

# Step 6: Print the users
if users:
    for user in users:
        print(f'User ID: {user.user_id}, Username: {user.user_name}, Email: {user.user_email}')
else:
    print('No users found')

# Step 7: Close the session
session.close()
```

Using the SQLAlchemy Declarative Method results in smaller and cleaner code and easy integration with object-oriented programming.

Your application structure should be like the following:

```text
tracker
├── tracker_01
├── ...
├── tracker_08a
|   ├── models
|   |   ├── __init__.py
|   |   ├── create_db.py
|   |   └── user.py
|   ├── static
|   |   ├── css
|   |   |   └── main.css
|   |   ├── img
|   |   |   ├── favicon.ico
|   |   |   └── logo.png
|   |   └── js
|   |       └── main.js
|   ├── tests
|   |   ├── __init__.py
|   |   └── test_app.py
|   ├── templates
|   |   ├── error
|   |   |   ├── 404.html
|   |   |   └── 500.html
|   |   ├── main
|   |   |   └── index.html
|   |   └── base.html
|   ├── __init__.py
|   ├── config.py
|   └── profiler.py
├── tracker_logs
|   └── tracker_08_1234567890.1234567.log
├── venv
|   └── ...
├── .env
├── .flaskenv
├── .gitignore
├── hello.py
└── requirements.txt
```

Review the code and run your application. Do not forget to activate your Python virtual environment first!

> **NOTE** - Enclose options in quotation marks when using special characters.

- `python -B -m flask --app "tracker_08a:create_app(config_name='development', log_events=True)" run`
- `python -B -m flask --app "tracker_08a:create_app('development', True)" run`

Run your application using the `development` configuration, refresh the page, and terminate the application using <kbd>CTRL</kbd> +  <kbd>C</kbd>. Take a look at the log file in `tracker_logs`. You should see something like the following:

```text
"date_time", "server_ip", "process_id", "msg_level", "message"
"2024-11-03 18:38:21,123", "192.168.56.1", "17384", "INFO", "Starting tracker_08a application."
"2024-11-03 18:38:23,836", "192.168.56.1", "17384", "INFO", "/ requested by 127.0.0.1 using GET; 200 OK."
"2024-11-03 18:38:24,436", "192.168.56.1", "17384", "INFO", "/static/img/logo.png requested by 127.0.0.1 using GET; 200 OK."
"2024-11-03 18:38:24,440", "192.168.56.1", "17384", "INFO", "/static/css/main.css requested by 127.0.0.1 using GET; 200 OK."
"2024-11-03 18:38:24,440", "192.168.56.1", "17384", "INFO", "/static/js/main.js requested by 127.0.0.1 using GET; 200 OK."
"2024-11-03 18:38:35,856", "192.168.56.1", "17384", "INFO", "/index requested by 127.0.0.1 using GET; 200 OK."
"2024-11-03 18:38:35,868", "192.168.56.1", "17384", "INFO", "/static/css/main.css requested by 127.0.0.1 using GET; 304 NOT MODIFIED."
"2024-11-03 18:38:35,870", "192.168.56.1", "17384", "INFO", "/static/img/logo.png requested by 127.0.0.1 using GET; 304 NOT MODIFIED."
"2024-11-03 18:38:35,871", "192.168.56.1", "17384", "INFO", "/static/js/main.js requested by 127.0.0.1 using GET; 304 NOT MODIFIED."
"2024-11-03 18:38:35,881", "192.168.56.1", "17384", "INFO", "/static/img/logo.png requested by 127.0.0.1 using GET; 304 NOT MODIFIED."
```

The HTTP response code `304 NOT MODIFIED` means that the server found a cached copy of the resource, like a favicon, so it did not request a new version from the server. This speeds up rendering the page. On most browsers, if you want the application to re-request the resource, press <kbd>Shift</kbd> <kbd>F5</kbd>; that forces the application to ignore the cache and retrieve a fresh version of the web page.

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by presssing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.

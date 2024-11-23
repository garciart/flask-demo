# Tracker_09

This is a demo of a Flask application that incorporates a database.

> **NOTE** - Remember to activate your Python virtual environment first:
>
> - `source .venv/bin/activate` (Linux)
> - `.venv/Scripts/activate` (Windows)

The purpose of the Tracker application is to track course assignments and, in order to do that, it needs a database.

-----

Short version:

We are using SQLite, a relational database that is built into the Python Standard Library.
We are using SQLAlchemy, an open-source Python library that provides an SQL toolkit and an Object Relational Mapper for database interactions.
There are several ways for Flask to interact with a database: the Raw SQL Method, the SQL with Classes Method, the SQLAlchemy Imperative (Classical) Method, and the SQLAlchemy Declarative Method
Using the SQLAlchemy Declarative Method results in smaller and cleaner code and easy integration with object-oriented programming.

To get started, install the SQLAlchemy library:

```shell
python -m pip install Flask-SQLAlchemy
python -m pip freeze > requirements.txt
```

In addition, you may eventually need to modify your database, like when you need to add columns, etc. To "transfer" your data to your new schema without losing data, you perform a database *migration*. To reduce the chances of issues with future migrations, perform an initial migration before you run the application:

```shell
# Check the application for issues
python -B -m pylint tracker_09
# Add Flask database migration package
python -m pip install Flask-Migrate
# Initialize migration support for the application
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_09 db init --directory tracker_09/migrations
python -B -m flask --app tracker_09 db init -d tracker_09/migrations
# Perform an initial migration to capture the current schema of the database
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_09 db migrate --message "Initial migration" --directory tracker_09/migrations
python -B -m flask --app tracker_09 db migrate -m "Initial migration" -d tracker_09/migrations
# Apply any pending migrations to the database.
# If using older command syntax, uncomment below:
# python -B -m flask --app tracker_09 db upgrade --directory tracker_09/migrations
python -B -m flask --app tracker_09 db upgrade -d tracker_09/migrations
# For help with any of these commands, use python -B -m flask --app tracker_09 db --help
```

That will create a `migrations` directory in your package (`tracker_09`) directory.

Your application structure should be like the following:

```text
tracker
├── .venv
|   └── ...
├── tracker_01
├── ...
├── tracker_09
|   ├── migrations
|   ├── models
|   |   ├── __init__.py
|   |   ├── create_db.py
|   |   └── member.py
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
|   └── tracker_09_1234567890.1234567.log
├── .coverage
├── .coveragerc
├── .env
├── .env_alt
├── .flaskenv
├── __init__.py
├── hello.py
└── requirements.txt
```

Check the code for issues, then run your application. Do not forget to activate your Python virtual environment first!

```shell
# Run the unit tests found in the `tests` directory using Coverage
coverage run -m unittest --verbose --buffer tracker_09/tests/test_app.py
# See the coverage report in the console
coverage report -m
# Profile the application using the built-in Werkzeug profiler:
python -B -m flask --app "tracker_09:create_app('profiler')" run --without-threads
# Run the Flask application using HTML files found in the `templates` directory
python -B -m flask --app tracker_09 run
```

Open a browser and navigate to <http://127.0.0.1:5000> to view. Stop the Werkzeug server between runs by pressing <kbd>CTRL</kbd> +  <kbd>C</kbd>. When you are finished, move on to the next version.

-----

Long version:

First, there was the Raw SQL Method:

```python
"""Raw SQL Method
"""

import sqlite3

# Step 1: Connect to the SQLite database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Step 2: Create the Member table
cursor.execute('''
CREATE TABLE IF NOT EXISTS member (
    member_id INTEGER PRIMARY KEY,
    member_name TEXT NOT NULL UNIQUE,
    member_email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL
)
''')

# Step 3: Add a member
cursor.execute('''
INSERT INTO member (member_name, member_email, password_hash)
VALUES (?, ?, ?)
''', ('john_doe', 'john@example.com', 'hashed_password'))

# Step 4: Commit the changes
conn.commit()

# Step 5: Fetch all members
cursor.execute('SELECT * FROM member')
members = cursor.fetchall()
print(members)

# Step 6: Close the connection
conn.close()
```

Then, there was the SQL with Classes Method:

```python
"""SQL and Classes method
"""

import sqlite3

class Member:
    def __init__(self, member_id=None, member_name=None, member_email=None, password_hash=None):
        self.member_id = member_id
        self.member_name = member_name
        self.member_email = member_email
        self.password_hash = password_hash

    @classmethod
    def create_table(cls, cursor):
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS member (
            member_id INTEGER PRIMARY KEY,
            member_name TEXT NOT NULL UNIQUE,
            member_email TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL
        )
        ''')

    @classmethod
    def insert(cls, cursor, member_name, member_email, password_hash):
        cursor.execute('''
        INSERT INTO member (member_name, member_email, password_hash)
        VALUES (?, ?, ?)
        ''', (member_name, member_email, password_hash))

    @classmethod
    def get_all(cls, cursor):
        cursor.execute('SELECT * FROM member')
        return cursor.fetchall()

# Step 1: Connect to the SQLite database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Step 2: Create the Member table
Member.create_table(cursor)

# Step 3: Add a member
Member.insert(cursor, 'john_doe', 'john@example.com', 'hashed_password')

# Step 4: Commit the changes
conn.commit()

# Step 5: Fetch all members
members = Member.get_all(cursor)
print(members)

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

member_table = Table(
    "member",
    mapper_registry.metadata,
    Column("member_id", Integer, primary_key=True),
    Column("member_name", String(64), nullable=False, unique=True),
    Column("member_email", String(320), nullable=False, unique=True),
    Column("password_hash", String(128), nullable=False),
)

# Define a class (no need to add any fields here since we're using the Table-based mapping)
class Member:
    pass

# Map the class to the table
mapper_registry.map_imperatively(Member, member_table)

# Step 1: Connect to the SQLite database and create the session
engine = create_engine('sqlite:///your_database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Step 2: Create the table in the database (if not exists)
mapper_registry.metadata.create_all(engine)  # Creates the table if it doesn't exist

# Step 3: Add a new member
new_member = {
    'member_name': 'john_doe',
    'member_email': 'john@example.com',
    'password_hash': 'hashed_password',
}

# Insert the new member into the table
session.execute(member_table.insert().values(new_member))

# Commit the changes
session.commit()

# Step 4: Fetch all members
result = session.execute(member_table.select())
members = result.fetchall()  # Fetch all rows

# Check if we found any members and print them
if members:
    for member in members:
        print(f'Member found: {member}')  # Each `member` is a Row object, print as is or extract columns
else:
    print('No members found')

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
class Member(DeclarativeBase):
    __tablename__ = "member"

    member_id: Mapped[int] = mapped_column(primary_key=True)
    member_name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    member_email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False)

# Step 2: Set up the database engine and session
engine = create_engine('sqlite:///your_database.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

# Step 3: Create the tables (if they don't exist)
Base.metadata.create_all(engine)

# Step 4: Insert a new member into the database
new_member = Member(member_name='john_doe', member_email='john@example.com', password_hash='hashed_password')
session.add(new_member)  # Add the member object to the session
session.commit()  # Commit the transaction to persist the member

# Step 5: Query all members from the database
members = session.query(Member).all()  # Fetch all members

# Step 6: Print the members
if members:
    for member in members:
        print(f'Member ID: {member.member_id}, Member Name: {member.member_name}, Email: {member.member_email}')
else:
    print('No members found')

# Step 7: Close the session
session.close()
```

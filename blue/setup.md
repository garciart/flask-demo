# Flask Application Walkthrough

This Flask application will allow you to administer courses and course access using a Flask front-end or application programming interface (API) calls.

-----

## Environment Setup

1. Create the virtual environment:

   - Windows:

       ```pwsh
       mkdir -p blue
       cd blue
       python -m venv $PWD/venv
       venv/Scripts/activate
       Set-Alias -Name python3 -Value python
       ```

   - Linux

       ```bash
       mkdir -p blue
       cd blue
       python3 -m venv $PWD/venv
       source venv/bin/activate
       ```

2. Install packages:

    ```sh
    python3 -m pip install --upgrade pip
    python3 -m pip install flask
    python3 -m pip install python-dotenv
    ```

3. Save requirements:

    ```sh
    python3 -m pip freeze > requirements.txt
    # Test: You should get a 'Requirement already satisfied' message
    python3 -m pip install -r requirements.txt
    ```

-----

## Add Initial Files

1. Create initial files and folder structure:

    | File/Folder | Notes |
    | ----------- | ----- |
    | `.flaskenv` | During development, set environment variables in this file instead of changing the state of the base OS. The `python-dotenv` package will allow Flask to 'read' the variables as though they were set in the OS, preserving the state of the base OS. Normally, this file *is not* committed to source control. |
    | `.gitignore` | Contains a list of files that you do not want to commit to source control. |
    | `app.py` | The entry point of the application (i.e., `python -B -m flask --app blue_app run`). |
    | `blue_app/config.py` | Contains variables shared by multiple application files. |
    | `blue_app/__init__.py` | Initializes the Python scripts in the `blue_app` directory as modules and acts as the application factory. |

    Your application tree should look like the following:

    ```txt
    blue
    ├── blue_app
    |   ├── __init__.py
    |   └── config.py
    ├── venv
    |   └── ...
    ├── .flaskenv
    ├── .gitignore
    ├── app.py
    └── requirements.txt
    ```

2. Run the application:

    ```sh
    python -B -m flask --app blue_app run
    ```

3. Open a browser and navigate to <http://127.0.0.1:5000/>. The message, "Hello, World!", should appear.

4. Press <kbd>Ctrl</kbd> + <kbd>C</kbd> to stop the server when finished.

-----

## Add Static Files and Templates

1. Add Static Files and Templates:

    ```shell
    mkdir -p blue_app/static
    mkdir -p blue_app/templates
    ```

    | File/Folder | Notes |
    | ----------- | ----- |
    | `static` | Contains static files, like Cascading Style Sheets (CSS), images, and scripts, used by HTML files. |
    | `templates` | Contains HTML files. |
    | `templates/demo_base.html` | Contains HTML code that is common to more than one web page. |
    | `templates/demo/demo_child.html` | Contains HTML content in Jinja2 template blocks. When the page renders, Flask replaces the placeholders in `demo_base.html` with the contents of this file. |
    | `logs` | Contains logs of Flask actions. |

    Your application tree should look like the following:

    ```txt
    blue
    ├── blue_app
    |   ├── static
    |   |   ├── css
    |   |   |   └── demo.css
    |   |   ├── img
    |   |   |   ├── favicon.ico
    |   |   |   └── logo.png
    |   |   ├── js
    |   |   |   └── demo.js
    |   ├── templates
    |   |   ├── demo
    |   |   |   └── demo_child.html
    |   |   └── demo_base.html
    |   ├── __init__.py
    |   └── config.py
    ├── logs
    ├── venv
    |   └── ...
    ├── .flaskenv
    ├── .gitignore
    ├── app.py
    └── requirements.txt
    ```

2. Run the application:

    ```sh
    python -B -m flask --app blue_app run
    ```

3. Open a browser and navigate to <http://127.0.0.1:5000/demo>. The formatted web page should appear.

4. Press <kbd>Ctrl</kbd> + <kbd>C</kbd> to stop the server when finished.

-----

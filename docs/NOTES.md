# Notes

-----

## Environment Setup

1. Create the virtual environment:

   - Windows:

       ```pwsh
       mkdir -p tracker
       cd tracker
       python<version> -m venv $PWD/.venv
       .venv/Scripts/activate
       ```

   - Linux

       ```bash
       mkdir -p tracker
       cd tracker
       python<version> -m venv $PWD/.venv
       source .venv/bin/activate
       ```

2. Install packages:

    ```shell
    python -m pip install --upgrade pip
    python -m pip install flask
    python -m pip install python-dotenv
    ```

3. Save requirements:

    ```shell
    python -m pip freeze > requirements.txt
    # Test: You should get a 'Requirement already satisfied' message
    python -m pip install -r requirements.txt
    ```

```shell
python3.12 -m venv $PWD/.venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install flask
python -m pip install python-dotenv
python -m pip install coverage
python -m pip install Flask-SQLAlchemy
python -m pip install Flask-Migrate
python -m pip freeze > requirements.txt
```
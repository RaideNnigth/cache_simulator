@echo off

rem Set the environment variables
set VENV_FOLDER=venv
set APP_PATH=src\app.py
set REQUIREMENTS_FILE=./requirements.txt

pip install -r requirements.txt
echo Requirements installed.
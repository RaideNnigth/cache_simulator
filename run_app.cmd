@echo off

rem Set the environment variables
set VENV_FOLDER=venv
set APP_PATH=src\app.py
set REQUIREMENTS_FILE=requirements.txt

echo Virtual environment folder: %VENV_FOLDER%
echo App path: %APP_PATH%

rem Check if virtual environment exists
if not exist %VENV_FOLDER%\Scripts\activate (
    echo Virtual environment not found. Creating...
    python -m venv %VENV_FOLDER%
) else (
    echo Virtual environment found. Activating...
)

rem Activate the virtual environment
call %VENV_FOLDER%\Scripts\activate

echo Virtual environment activated.


echo Installing requirements...
call %VENV_FOLDER%\Scripts\activate
pip install -r requirements.txt
echo Requirements installed.

echo Running the Flask app...

rem Run the Flask app
python %APP_PATH%

echo App stopped.
echo Deactivating the virtual environment...

rem Deactivate the virtual environment
deactivate

echo Virtual environment deactivated.
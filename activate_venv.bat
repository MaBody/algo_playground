@echo off

rem Set the name of your Python virtual environment
set VENV_NAME=algo-playground-env

set VENV_DIR=C:\Users\Mattis\Envs
set VENV_PATH=%VENV_DIR%\%VENV_NAME%

rem Check if the virtual environment exists
if not exist "%VENV_PATH%" (
    echo Virtual environment %VENV_NAME% does not exist yet. Initializing...
    pushd %VENV_DIR%
    python -m venv %VENV_NAME%
    popd
    echo Initialized %VENV_NAME%!
)

rem Activate the virtual environment
call "%VENV_PATH%\Scripts\activate.bat"

rem Optional: Display a message indicating the virtual environment is activated
echo %VENV_NAME% activated successfully.

rem Keep the command prompt open
cmd /k
@set VENV_NAME=venv
@set REQ_FILE=requirements.txt

@if exist %VENV_NAME% goto UPDATE_VENV

:INSTALL_VENV
@python -m pip install virtualenv
@python -m virtualenv %VENV_NAME%

:UPDATE_VENV
@call %VENV_NAME%/Scripts/activate.bat
@python -m pip install -r %REQ_FILE%
@deactivate
@echo:
@pause
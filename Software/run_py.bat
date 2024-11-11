@set VENV=venv

@echo Activating venv!
@call %VENV%\Scripts\activate.bat
@call python main.py %*
@echo Deactivating venv!
@deactivate
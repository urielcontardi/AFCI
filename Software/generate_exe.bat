set OUTPUT_DIR=dist
set APP_NAME=ARCGenerator
set VENV=venv

if not exist %VENV% (
    echo Please run "generate_venv.bat" first!
    goto END
)

:GENERATE_EXE
call %VENV%\Scripts\activate

REM ARGS are required because screeninfo isn't found for some reason
REM It only was found after the venv was setup
set ARGS=--paths venv\Lib\site-packages --hidden-import screeninfo

python -m PyInstaller --onefile --windowed --noconfirm %ARGS% --name %APP_NAME%  main.py

REM Verify if executable was generated
if ERRORLEVEL 1 (
    echo Error to generate executable
    goto END
)

:END
echo:
pause
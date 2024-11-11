set OUTPUT_DIR=dist
set APP_NAME=ARC Generator
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

REM Set Icon 
set ICON=statics\weg_logo.ico

REM Include data and statics folders in the executable
set DATA=--add-data "data;data" --add-data "statics;statics"

python -m PyInstaller --onefile --windowed --noconfirm %ARGS% %DATA% --name %APP_NAME% --icon %ICON% main.py

REM Verify if executable was generated
if ERRORLEVEL 1 (
    echo Error to generate executable
    goto END
)

:END
echo:
pause
@echo off
echo.
echo ========================================
echo    BANQUE NATIONALE - Demarrage
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou non dans le PATH
    echo Telechargez Python depuis: https://www.python.org
    pause
    exit /b 1
)

echo [OK] Python detecte

REM Check if virtual environment exists
if not exist "venv" (
    echo [INFO] Creation de l'environnement virtuel...
    python -m venv venv
    if errorlevel 1 (
        echo [ERREUR] Impossible de creer l'environnement virtuel
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [INFO] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERREUR] Impossible d'activer l'environnement virtuel
    pause
    exit /b 1
)

REM Install requirements
echo [INFO] Installation des dependances...
pip install -q -r requirements.txt
if errorlevel 1 (
    echo [ERREUR] Impossible d'installer les dependances
    pause
    exit /b 1
)

REM Start the application
echo.
echo [OK] Tout est pret!
echo.
echo ========================================
echo    Demarrage de l'application...
echo ========================================
echo.
echo Ouvrez votre navigateur et allez a:
echo http://localhost:5000
echo.
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

python app.py

pause

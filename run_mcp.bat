@echo off
echo Fûinjutsu - Interface MCP

REM Vérifier si un environnement virtuel existe déjà
if not exist venv (
    echo Création d'un environnement virtuel...
    python -m venv venv
    echo Environnement virtuel créé.
)

REM Activer l'environnement virtuel
echo Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Installer les dépendances si nécessaire
if not exist venv\.dependencies_installed (
    echo Installation des dépendances...
    pip install -r requirements.txt
    echo. > venv\.dependencies_installed
    echo Dépendances installées.
) else (
    echo Les dépendances sont déjà installées.
)

REM Lancer l'application MCP
echo Lancement de l'interface MCP Fûinjutsu...
python mcp_app.py

REM Désactiver l'environnement virtuel à la sortie
call deactivate
echo Application fermée. Environnement virtuel désactivé.
pause
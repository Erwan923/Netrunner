@echo off
echo Fuinjutsu - Configuration Docker

REM Vérifier si Docker est installé
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Docker n'est pas installe. Veuillez installer Docker avant de continuer.
    exit /b 1
)

REM Vérifier si Docker Compose est installé
where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Docker Compose n'est pas installe. Veuillez installer Docker Compose avant de continuer.
    exit /b 1
)

REM Demander les clés API à l'utilisateur
set /p huggingface_key="Entrez votre cle API HuggingFace: "
set /p openai_key="Entrez votre cle API OpenAI (optionnel): "

REM Créer ou mettre à jour le fichier .env
echo HUGGINGFACE_API_KEY=%huggingface_key%> .env
echo OPENAI_API_KEY=%openai_key%>> .env

echo Configuration terminee. Vous pouvez maintenant lancer l'application avec:
echo docker-compose up -d   # Pour lancer l'interface cyberpunk
pause
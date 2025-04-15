#!/bin/bash

# Vérifier si un environnement virtuel existe déjà
if [ ! -d "venv" ]; then
    echo "Création d'un environnement virtuel..."
    python -m venv venv
    echo "Environnement virtuel créé."
fi

# Activer l'environnement virtuel
echo "Activation de l'environnement virtuel..."
source venv/bin/activate

# Installer les dépendances si nécessaire
if [ ! -f "venv/.dependencies_installed" ]; then
    echo "Installation des dépendances..."
    pip install -r requirements.txt
    touch venv/.dependencies_installed
    echo "Dépendances installées."
else
    echo "Les dépendances sont déjà installées."
fi

# Lancer l'application MCP
echo "Lancement de l'interface MCP Fûinjutsu..."
python mcp_app.py

# Désactiver l'environnement virtuel à la sortie
deactivate
echo "Application fermée. Environnement virtuel désactivé."
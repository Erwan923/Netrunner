#!/bin/bash

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "Docker n'est pas installé. Veuillez installer Docker avant de continuer."
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose n'est pas installé. Veuillez installer Docker Compose avant de continuer."
    exit 1
fi

# Demander les clés API à l'utilisateur
read -p "Entrez votre clé API HuggingFace: " huggingface_key
read -p "Entrez votre clé API OpenAI (optionnel): " openai_key

# Créer ou mettre à jour le fichier .env
echo "HUGGINGFACE_API_KEY=$huggingface_key" > .env
echo "OPENAI_API_KEY=$openai_key" >> .env
echo "Configuration terminée. Vous pouvez maintenant lancer l'application avec:"
echo "docker-compose up -d   # Pour lancer l'interface cyberpunk"
echo "docker-compose up -d                      # Pour les deux interfaces"
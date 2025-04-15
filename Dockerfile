FROM python:3.10-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de dépendances en premier pour optimiser la mise en cache
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Créer les dossiers nécessaires et définir les permissions
RUN mkdir -p /app/config /app/data \
    && chmod -R 755 /app

# Copier le reste des fichiers du projet
COPY . .

# Définir les variables d'environnement par défaut
ENV HUGGINGFACE_API_KEY=""
ENV OPENAI_API_KEY=""
ENV ANTHROPIC_API_KEY=""
ENV GOOGLE_API_KEY=""
ENV MISTRAL_API_KEY=""
ENV COHERE_API_KEY=""
ENV HOST="0.0.0.0"
ENV PORT=5000
ENV CONFIG_PATH="/app/config/config.json"
ENV DOCKER_ENV="true"

# Exposer les ports
EXPOSE 5000  # Taipy pour les interfaces standard et MCP
EXPOSE 8000  # Serveur HTTP pour l'interface cyberpunk
EXPOSE 5001  # Pour l'API REST des MCPs

# Volume pour persister la configuration et les données
VOLUME ["/app/config", "/app/data"]

# Mettre en place un utilisateur non-root pour des raisons de sécurité
RUN groupadd -r fuinjutsu && useradd -r -g fuinjutsu fuinjutsu
RUN chown -R fuinjutsu:fuinjutsu /app
USER fuinjutsu

# Vérifications de santé
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl -f http://localhost:5000/ || exit 1

# Commande par défaut (sera remplacée dans docker-compose.yml)
CMD ["python", "cyberpunk_app.py"]
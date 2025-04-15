# Fûinjutsu - Interface Cyberpunk pour LLMs

Fûinjutsu est une interface immersive inspirée de l'esthétique cyberpunk pour utiliser plusieurs modèles de langage (LLMs). Cette implémentation utilise l'API HuggingFace avec le modèle google/flan-t5-xxl, mais peut facilement être adaptée à d'autres LLMs comme OpenAI GPT-3.5.

blob:moz-extension://44c67e95-7969-492e-ab8f-6bf5d02ed97d/95048fc7-788e-42e8-b3d1-d871dc8c9594

## Interface

Fûinjutsu propose une interface cyberpunk immersive avec une esthétique futuriste et des fonctionnalités avancées pour interagir avec différents modèles de langage.

## Installation

### Installation standard

1. Clonez ce dépôt :
```bash
git clone <url-du-repo>
cd Fûinjutsu
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

### Installation avec Docker

Vous pouvez également utiliser Docker pour déployer l'application :

```bash
# Cloner le dépôt
git clone <url-du-repo>
cd Fûinjutsu

# Construire et lancer les conteneurs
docker-compose up -d
```

Cette commande lancera tous les services nécessaires :
- Interface Cyberpunk sur http://localhost:5000 et http://localhost:8000
- Interface MCP sur http://localhost:5001
- Proxy Nginx sur http://localhost:80 pour unifier l'accès

### Déploiement sur Kubernetes

Fûinjutsu peut être déployé sur Kubernetes à l'aide du chart Helm fourni :

```bash
# Depuis le répertoire du projet
helm install fuinjutsu ./helm/fuinjutsu

# Ou pour personnaliser le déploiement
helm install fuinjutsu ./helm/fuinjutsu -f values.yaml
```

Pour plus d'informations sur le déploiement Kubernetes, consultez le [README du chart Helm](./helm/README.md).

## Configuration

### Configuration des clés API

Plusieurs options s'offrent à vous pour configurer les clés API des différents services LLM :

#### 1. Via l'interface MCP

L'option la plus simple est d'utiliser l'interface MCP pour gérer vos clés API :

1. Lancez l'application avec `./run_mcp.sh` ou `run_mcp.bat`
2. Accédez à la page "Gérer les clés API"
3. Ajoutez vos clés pour HuggingFace, OpenAI, etc.

Les clés sont stockées de manière sécurisée dans un fichier de configuration local.

#### 2. Via des variables d'environnement

Vous pouvez définir les clés API via des variables d'environnement :

```bash
# Sous Linux/macOS
export HUGGINGFACE_API_KEY="votre-clé-huggingface"
export OPENAI_API_KEY="votre-clé-openai"
./run.sh  # ou ./run_mcp.sh

# Sous Windows (PowerShell)
$env:HUGGINGFACE_API_KEY="votre-clé-huggingface"
$env:OPENAI_API_KEY="votre-clé-openai"
.\run.bat  # ou .\run_mcp.bat
```

#### 3. Via Docker Compose

Si vous utilisez Docker, vous pouvez configurer les clés dans un fichier `.env` à la racine du projet :

```
HUGGINGFACE_API_KEY=votre-clé-huggingface
OPENAI_API_KEY=votre-clé-openai
ANTHROPIC_API_KEY=votre-clé-anthropic
GOOGLE_API_KEY=votre-clé-google
MISTRAL_API_KEY=votre-clé-mistral
COHERE_API_KEY=votre-clé-cohere
```

Puis lancer Docker Compose :

```bash
docker-compose up -d
```

#### 4. Via le chart Helm

Pour un déploiement Kubernetes, vous pouvez configurer les clés dans votre fichier `values.yaml` :

```yaml
apiKeys:
  keys:
    HUGGINGFACE_API_KEY: "votre-clé-huggingface"
    OPENAI_API_KEY: "votre-clé-openai"
    # etc.
```

### Obtention des clés API

- **HuggingFace** : [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- **OpenAI** : [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Anthropic** : [console.anthropic.com/account/keys](https://console.anthropic.com/account/keys)
- **Google AI** : [ai.google.dev](https://ai.google.dev/)
- **Mistral AI** : [console.mistral.ai/api-keys](https://console.mistral.ai/api-keys/)
- **Cohere** : [dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys)

## Utilisation

Pour lancer l'application avec l'interface cyberpunk, vous pouvez utiliser les scripts fournis :

**Sur Linux/macOS :**
```bash
./run.sh
```

**Sur Windows :**
```
run.bat
```

Ces scripts vont :
1. Créer un environnement virtuel si nécessaire
2. Installer les dépendances
3. Lancer l'application

Alternativement, vous pouvez lancer l'application manuellement :

```bash
python cyberpunk_app.py
```

Cette commande lancera une interface Taipy qui vous permettra de configurer les paramètres des modèles, puis de lancer l'interface cyberpunk dans votre navigateur web.

### Interface MCP (Model Context Protocol)

Fûinjutsu propose également une interface pour les MCPs (Model Context Protocol) qui permet d'utiliser des modules de traitement modulaires.

Pour lancer l'interface MCP :

**Sur Linux/macOS :**
```bash
./run_mcp.sh
```

**Sur Windows :**
```
run_mcp.bat
```

L'interface MCP vous permet de :
1. Sélectionner un MCP parmi ceux disponibles
2. Consulter sa documentation
3. Saisir un JSON d'entrée
4. Exécuter le MCP
5. Visualiser le résultat
6. Gérer vos clés API pour différents services LLM

Les MCPs sont également accessibles via une API REST :
```
POST /mcp/<nom_du_mcp>
Content-Type: application/json

{
  "param1": "valeur1",
  "param2": "valeur2"
}
```

#### Gestion des clés API

L'interface MCP inclut une page dédiée à la gestion des clés API pour différents services LLM :

- Ajout et modification de clés API pour HuggingFace, OpenAI, Anthropic, etc.
- Stockage sécurisé des clés dans un fichier de configuration chiffré
- Utilisation automatique des clés appropriées par les différents MCPs

Pour accéder à cette fonctionnalité, cliquez sur le bouton "Gérer les clés API" dans l'interface.

Vous pouvez également ouvrir directement le fichier `index.html` dans votre navigateur pour accéder à l'interface cyberpunk, mais certaines fonctionnalités comme les appels API ne fonctionneront pas sans le backend Python.

L'interface se compose de :
- Un panneau de conversation principal où vous pouvez interagir avec le LLM
- Une barre latérale avec des contrôles pour :
  - Effacer la conversation actuelle
  - Sauvegarder la conversation dans l'historique
  - Charger une conversation précédente depuis l'historique

## Fonctionnalités

- Interface de chat intuitive avec styles différenciés pour les messages utilisateur et IA
- Historique des conversations
- Thème sombre par défaut avec possibilité de basculer vers un thème clair
- Notifications pour les actions importantes

## Personnalisation

Vous pouvez personnaliser l'apparence de l'application en modifiant le fichier `cyberpunk-style.css`.

Pour utiliser un autre modèle de langage, modifiez les variables `API_URL` et adaptez les fonctions de requête dans `cyberpunk_app.py` selon les besoins du nouveau modèle.

## Extension

Ce projet peut être étendu pour prendre en charge d'autres LLMs comme :
- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude)
- Modèles locaux via Ollama
- Et bien d'autres !

### Exemple avec OpenAI

Un exemple d'implémentation avec l'API OpenAI est fourni dans le fichier `openai_example.py`. Pour l'utiliser :

1. Obtenez une clé API OpenAI sur [OpenAI Platform](https://platform.openai.com/api-keys)
2. Ouvrez le fichier `openai_example.py`
3. Remplacez `"your-openai-api-key"` par votre clé API
4. Exécutez l'exemple :
```bash
python openai_example.py
```

Cet exemple montre comment adapter l'application pour utiliser le modèle GPT-3.5 d'OpenAI au lieu de FLAN-T5.

## Structure du projet

### Fichiers principaux
- `cyberpunk_app.py` : Application pour lancer l'interface cyberpunk
- `index.html` : Structure HTML de l'interface cyberpunk
- `cyberpunk-style.css` : Styles CSS pour l'interface cyberpunk
- `mcp_app.py` : Application pour l'interface MCP (Model Context Protocol)
- `requirements.txt` : Dépendances du projet
- `run.sh` / `run.bat` : Scripts pour lancer l'interface cyberpunk
- `run_mcp.sh` / `run_mcp.bat` : Scripts pour lancer l'interface MCP

### MCPs (Model Context Protocol)
- `mcps/` : Dossier contenant les modules MCP
- `mcps/__init__.py` : Module d'initialisation pour charger les MCPs
- `mcps/text_translator.py` : MCP pour traduire du texte
- `mcps/sentiment_analyzer.py` : MCP pour analyser le sentiment d'un texte
- `mcps/text_summarizer.py` : MCP pour résumer un texte

### Exemples et utilitaires
- `openai_example.py` : Exemple d'implémentation avec OpenAI
- `api_example.py` : Exemple d'utilisation programmatique sans interface graphique

## Utilisation programmatique

### API LLM

Si vous souhaitez utiliser les fonctionnalités de requête LLM directement dans votre code sans passer par l'interface graphique, consultez le fichier `api_example.py`. Ce fichier contient des exemples de fonctions pour envoyer des requêtes aux API HuggingFace et OpenAI.

Pour utiliser ces fonctions :

```python
from api_example import query_huggingface, query_openai

# Exemple avec HuggingFace
response = query_huggingface("Translate 'Hello' to French")

# Exemple avec OpenAI
response = query_openai("Translate 'Hello' to French", "your-api-key")
```

### API MCP

Vous pouvez également utiliser les MCPs directement dans votre code :

```python
from mcps import load_mcps, execute_mcp

# Charger les MCPs
load_mcps()

# Exécuter un MCP
result = execute_mcp("text_translator", {
    "text": "Hello, how are you?",
    "source_lang": "en",
    "target_lang": "fr"
})
print(result)
```

Ou via l'API REST en utilisant n'importe quel client HTTP :

```python
import requests

# Appeler un MCP via l'API
response = requests.post(
    "http://localhost:5000/mcp/text_translator",
    json={
        "text": "Hello, how are you?",
        "source_lang": "en",
        "target_lang": "fr"
    }
)
print(response.json())
```

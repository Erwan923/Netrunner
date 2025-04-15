import requests
import json
import os
import webbrowser
import http.server
import socketserver
import threading
import datetime
from taipy.gui import Gui, State, notify, navigate

# Configuration de l'API HuggingFace
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_KEY', '[YOUR ACCESS TOKEN]')}"}

# Configuration de l'API OpenAI (pour l'exemple)
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "your-openai-api-key")
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
openai_headers = {
    "Authorization": f"Bearer {OPENAI_API_KEY}",
    "Content-Type": "application/json"
}

# Variables pour stocker les paramètres
model_settings = {
    "FLAN-T5": {
        "temperature": 0.7,
        "max_length": 150,
        "api_key": os.environ.get('HUGGINGFACE_API_KEY', '[YOUR ACCESS TOKEN]')
    },
    "GPT-3.5": {
        "temperature": 0.7,
        "max_length": 150,
        "api_key": os.environ.get('OPENAI_API_KEY', "your-openai-api-key")
    }
}

current_model = "FLAN-T5"

def query_huggingface(prompt, temperature=0.7, max_length=150):
    """
    Envoie une requête à l'API HuggingFace et retourne la réponse.
    
    Args:
        - prompt: Le prompt à envoyer à l'API.
        - temperature: Paramètre de température pour la génération.
        - max_length: Longueur maximale de la réponse.
        
    Returns:
        La réponse de l'API.
    """
    payload = {
        "inputs": prompt,
        "parameters": {
            "temperature": temperature,
            "max_length": max_length
        }
    }
    
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def query_openai(prompt, temperature=0.7, max_tokens=150):
    """
    Envoie une requête à l'API OpenAI et retourne la réponse.
    
    Args:
        - prompt: Le prompt à envoyer à l'API.
        - temperature: Paramètre de température pour la génération.
        - max_tokens: Nombre maximum de tokens dans la réponse.
        
    Returns:
        La réponse de l'API.
    """
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }
    
    try:
        response = requests.post(OPENAI_API_URL, headers=openai_headers, json=payload)
        return response.json()
    except Exception as e:
        return {"error": str(e)}

def process_query(model, prompt, temperature=0.7, max_length=150):
    """
    Traite une requête en fonction du modèle sélectionné.
    
    Args:
        - model: Le modèle à utiliser (FLAN-T5 ou GPT-3.5).
        - prompt: Le prompt à envoyer à l'API.
        - temperature: Paramètre de température pour la génération.
        - max_length: Longueur maximale de la réponse.
        
    Returns:
        La réponse du modèle.
    """
    if model == "FLAN-T5":
        response = query_huggingface(prompt, temperature, max_length)
        if isinstance(response, list) and len(response) > 0:
            return response[0]["generated_text"]
        elif "error" in response:
            return f"Erreur: {response['error']}"
        else:
            return f"Réponse inattendue: {response}"
    elif model == "GPT-3.5":
        response = query_openai(prompt, temperature, max_length)
        if "choices" in response and len(response["choices"]) > 0:
            return response["choices"][0]["message"]["content"]
        elif "error" in response:
            return f"Erreur: {response['error']}"
        else:
            return f"Réponse inattendue: {response}"
    else:
        return "Modèle non pris en charge."

# Serveur HTTP simple pour servir l'interface
class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        # Supprimer les logs pour éviter de polluer la console
        pass

def start_server(port=8000, directory=None):
    """
    Démarre un serveur HTTP simple pour servir l'interface.
    
    Args:
        - port: Le port sur lequel démarrer le serveur.
        - directory: Le répertoire contenant les fichiers à servir.
    """
    handler = SimpleHTTPRequestHandler
    
    # Configurer le répertoire
    if directory:
        os.chdir(directory)
    
    httpd = socketserver.TCPServer(("0.0.0.0", port), handler)
    print(f"Serveur démarré sur le port {port}")
    httpd.serve_forever()

def launch_interface():
    """
    Lance l'interface web dans le navigateur par défaut.
    """
    # Obtenir le chemin absolu du répertoire contenant les fichiers HTML/CSS
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Démarrer le serveur dans un thread séparé
    server_thread = threading.Thread(target=start_server, kwargs={
        'port': 8000,
        'directory': current_dir
    })
    server_thread.daemon = True
    server_thread.start()
    
    # Ouvrir le navigateur (désactivé dans Docker)
    if os.environ.get("DOCKER_ENV") != "true":
        webbrowser.open(f"http://localhost:8000/index.html")
    
    print("Interface lancée.")
    print("Accédez à http://localhost:8000/index.html dans votre navigateur.")
    print("Appuyez sur Ctrl+C pour quitter.")
    
    try:
        # Garder le programme en cours d'exécution
        while True:
            pass
    except KeyboardInterrupt:
        print("Serveur arrêté.")

# Interface Taipy pour les paramètres avancés
advanced_settings_page = """
<|toggle|theme|>

<|layout|columns=1 1|
<|
## Paramètres avancés de Fûinjutsu

### Modèle actuel: <|{current_model}|>

<|{current_model}|selector|lov=FLAN-T5;GPT-3.5|>

### Paramètres du modèle

**Température**: <|{model_settings[current_model]["temperature"]}|slider|min=0|max=1|step=0.1|>

**Longueur maximale**: <|{model_settings[current_model]["max_length"]}|number|>

**Clé API**: <|{model_settings[current_model]["api_key"]}|input|password=True|>

<|Sauvegarder les paramètres|button|on_action=save_settings|>
<|Lancer l'interface cyberpunk|button|on_action=launch_cyberpunk_interface|>
|>

<|
## Informations

L'interface cyberpunk de Fûinjutsu vous permet d'interagir avec différents modèles de langage dans un environnement visuellement immersif inspiré de l'esthétique cyberpunk.

### Fonctionnalités
- Interface utilisateur cyberpunk
- Support de plusieurs modèles de langage
- Personnalisation des paramètres
- Historique des conversations

### Modèles supportés
- FLAN-T5 (via HuggingFace)
- GPT-3.5 (via OpenAI)
- Plus à venir...

<|Retour à l'accueil|button|on_action=go_home|>
|>
|>
"""

def save_settings(state: State):
    """
    Sauvegarde les paramètres du modèle.
    
    Args:
        - state: L'état actuel de l'application.
    """
    # Mettre à jour les variables globales
    global API_URL, headers, OPENAI_API_KEY, openai_headers
    
    if state.current_model == "FLAN-T5":
        headers = {"Authorization": f"Bearer {state.model_settings[state.current_model]['api_key']}"}
    elif state.current_model == "GPT-3.5":
        OPENAI_API_KEY = state.model_settings[state.current_model]["api_key"]
        openai_headers = {
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json"
        }
    
    notify(state, "success", f"Paramètres du modèle {state.current_model} sauvegardés!")

def launch_cyberpunk_interface(state: State):
    """
    Lance l'interface cyberpunk.
    
    Args:
        - state: L'état actuel de l'application.
    """
    # Sauvegarder les paramètres avant de lancer l'interface
    save_settings(state)
    
    # Lancer l'interface dans un thread séparé
    interface_thread = threading.Thread(target=launch_interface)
    interface_thread.daemon = True
    interface_thread.start()
    
    notify(state, "info", "Interface cyberpunk lancée dans le navigateur!")

def go_home(state: State):
    """
    Retourne à la page d'accueil.
    
    Args:
        - state: L'état actuel de l'application.
    """
    navigate(state, "home")

# Page d'accueil
home_page = """
<|toggle|theme|>

<|layout|columns=1|
<|
# Fûinjutsu - Interface Unifiée pour LLMs

Bienvenue dans Fûinjutsu, une interface unifiée pour utiliser plusieurs modèles de langage (LLMs).

<|Lancer l'interface cyberpunk|button|on_action=launch_cyberpunk_interface|>
<|Paramètres avancés|button|on_action=go_to_settings|>
|>
|>
"""

def go_to_settings(state: State):
    """
    Navigue vers la page des paramètres.
    
    Args:
        - state: L'état actuel de l'application.
    """
    navigate(state, "settings")

# Configuration des pages
pages = {
    "/": home_page,
    "home": home_page,
    "settings": advanced_settings_page
}

if __name__ == "__main__":
    # Vérifier si le répertoire courant contient index.html
    if not os.path.exists("index.html"):
        print("Fichier index.html non trouvé. Le fichier sera servi depuis le répertoire actuel.")
    
    # Configuration du serveur Taipy
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    
    # Indiquer que nous sommes dans un environnement Docker
    if os.environ.get("HOST") == "0.0.0.0":
        os.environ["DOCKER_ENV"] = "true"
    
    # Lancer l'interface Taipy
    gui = Gui(pages=pages)
    gui.run(title="Fûinjutsu", dark_mode=True, host=host, port=port)
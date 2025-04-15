"""
Application Taipy pour la gestion des MCPs (Model Context Protocol)
Intègre également un endpoint Flask pour l'accès par API
"""

import json
import os
from typing import Dict, Any, List
from taipy.gui import Gui, State, notify, navigate
from flask import Flask, request, jsonify

# Importer les MCPs
from mcps import load_mcps, get_all_mcps, get_mcp, execute_mcp

# Importer le gestionnaire de configuration
from utils.config_manager import config_manager

# Définir les services LLM pris en charge
LLM_SERVICES = [
    {"id": "huggingface", "name": "HuggingFace", "description": "API HuggingFace pour les modèles FLAN-T5 et autres"},
    {"id": "openai", "name": "OpenAI", "description": "API OpenAI pour les modèles GPT-3.5, GPT-4, etc."},
    {"id": "anthropic", "name": "Anthropic", "description": "API Anthropic pour les modèles Claude"},
    {"id": "google", "name": "Google AI", "description": "API Google AI pour les modèles Gemini et PaLM"},
    {"id": "mistral", "name": "Mistral AI", "description": "API Mistral AI pour les modèles Mistral"},
    {"id": "cohere", "name": "Cohere", "description": "API Cohere pour les modèles de langage et d'embeddings"}
]

# Initialisation des variables
mcps = load_mcps()
selected_mcp = None
input_json = "{}"
result_json = ""
mcp_description = ""
mcp_input_schema = ""
mcp_output_schema = ""

# Variables pour la page des clés API
api_keys_table = []
new_service_name = ""
new_service_key = ""
selected_service = None

def parse_input_json(input_str: str) -> Dict[str, Any]:
    """
    Valide et parse une chaîne JSON
    
    Args:
        input_str: La chaîne JSON à parser
        
    Returns:
        Le dictionnaire parsé ou un dictionnaire d'erreur
    """
    try:
        return json.loads(input_str)
    except json.JSONDecodeError as e:
        return {"error": f"Erreur de syntaxe JSON: {str(e)}"}

def format_json(data: Dict[str, Any]) -> str:
    """
    Formate un dictionnaire en JSON avec indentation
    
    Args:
        data: Le dictionnaire à formater
        
    Returns:
        La chaîne JSON formatée
    """
    return json.dumps(data, indent=2, ensure_ascii=False)

def execute_selected_mcp(state: State) -> None:
    """
    Exécute le MCP sélectionné avec les données d'entrée
    
    Args:
        state: L'état actuel de l'application
    """
    if not state.selected_mcp:
        notify(state, "error", "Aucun MCP sélectionné")
        return
    
    # Parser les données d'entrée
    input_data = parse_input_json(state.input_json)
    if "error" in input_data:
        state.result_json = format_json(input_data)
        notify(state, "error", input_data["error"])
        return
    
    # Exécuter le MCP
    try:
        result = execute_mcp(state.selected_mcp, input_data)
        state.result_json = format_json(result)
        notify(state, "success", f"MCP '{state.selected_mcp}' exécuté avec succès")
    except Exception as e:
        error_data = {"error": str(e)}
        state.result_json = format_json(error_data)
        notify(state, "error", str(e))

def update_mcp_info(state: State) -> None:
    """
    Met à jour les informations du MCP sélectionné
    
    Args:
        state: L'état actuel de l'application
    """
    if not state.selected_mcp:
        state.mcp_description = ""
        state.mcp_input_schema = ""
        state.mcp_output_schema = ""
        return
    
    mcp = get_mcp(state.selected_mcp)
    if mcp:
        metadata = mcp["metadata"]
        state.mcp_description = metadata.get("description", "Aucune description disponible")
        
        # Formater le schéma d'entrée
        input_schema = metadata.get("input_schema", {})
        state.mcp_input_schema = "\n".join([f"- {key}: {value}" for key, value in input_schema.items()])
        
        # Formater le schéma de sortie
        output_schema = metadata.get("output_schema", {})
        state.mcp_output_schema = "\n".join([f"- {key}: {value}" for key, value in output_schema.items()])
        
        # Préparer un exemple JSON d'entrée basé sur le schéma
        example_input = {}
        for key in input_schema:
            if "str" in input_schema[key].lower():
                example_input[key] = ""
            elif "int" in input_schema[key].lower():
                example_input[key] = 0
            elif "float" in input_schema[key].lower():
                example_input[key] = 0.0
            elif "bool" in input_schema[key].lower():
                example_input[key] = False
            elif "list" in input_schema[key].lower() or "array" in input_schema[key].lower():
                example_input[key] = []
            elif "dict" in input_schema[key].lower() or "object" in input_schema[key].lower():
                example_input[key] = {}
        
        state.input_json = format_json(example_input)

def on_change_mcp(state: State, var_name: str, var_value: str) -> None:
    """
    Gère le changement de MCP sélectionné
    
    Args:
        state: L'état actuel de l'application
        var_name: Le nom de la variable modifiée
        var_value: La nouvelle valeur
    """
    if var_name == "selected_mcp":
        update_mcp_info(state)

def reload_mcps(state: State) -> None:
    """
    Recharge tous les MCPs
    
    Args:
        state: L'état actuel de l'application
    """
    global mcps
    mcps = load_mcps()
    state.selected_mcp = None
    state.input_json = "{}"
    state.result_json = ""
    update_mcp_info(state)
    notify(state, "info", "MCPs rechargés")

def go_home(state: State) -> None:
    """
    Retourne à la page d'accueil
    
    Args:
        state: L'état actuel de l'application
    """
    navigate(state, "home")

def go_to_mcps(state: State) -> None:
    """
    Navigue vers la page des MCPs
    
    Args:
        state: L'état actuel de l'application
    """
    navigate(state, "mcps")

def go_to_api_keys(state: State) -> None:
    """
    Navigue vers la page des clés API
    
    Args:
        state: L'état actuel de l'application
    """
    load_api_keys(state)
    navigate(state, "api_keys")

# Fonctions pour la gestion des clés API
def load_api_keys(state: State) -> None:
    """
    Charge les clés API depuis le gestionnaire de configuration
    
    Args:
        state: L'état actuel de l'application
    """
    # Récupérer toutes les clés API
    api_keys_dict = config_manager.get_all_api_keys()
    
    # Convertir en liste de dictionnaires pour l'affichage dans un tableau
    api_keys_list = []
    for service_id, key in api_keys_dict.items():
        # Trouver le nom complet du service s'il existe dans notre liste
        service_name = service_id
        for service in LLM_SERVICES:
            if service["id"] == service_id:
                service_name = service["name"]
                break
        
        # Masquer la clé API pour la sécurité
        masked_key = "•" * 8 + key[-4:] if key and len(key) > 4 else "•" * 12
        
        api_keys_list.append({
            "Service": service_name,
            "ID": service_id,
            "Clé": masked_key,
            "Status": "Valide" if key else "Non définie"
        })
    
    state.api_keys_table = api_keys_list

def select_api_key(state: State, row_id) -> None:
    """
    Sélectionne une clé API dans le tableau
    
    Args:
        state: L'état actuel de l'application
        row_id: L'identifiant de la ligne sélectionnée
    """
    if row_id and len(state.api_keys_table) > row_id:
        service_id = state.api_keys_table[row_id]["ID"]
        state.selected_service = service_id
        state.new_service_name = service_id
        
        # Récupérer la clé complète (non masquée)
        full_key = config_manager.get_api_key(service_id)
        state.new_service_key = full_key if full_key else ""
        
        notify(state, "info", f"Service '{service_id}' sélectionné")

def save_api_key(state: State) -> None:
    """
    Sauvegarde une clé API
    
    Args:
        state: L'état actuel de l'application
    """
    if not state.new_service_name:
        notify(state, "error", "Vous devez spécifier un nom de service")
        return
    
    # Normaliser le nom du service (en minuscules, sans espaces)
    service_id = state.new_service_name.lower().strip().replace(" ", "_")
    
    # Enregistrer la clé
    config_manager.set_api_key(service_id, state.new_service_key)
    
    # Recharger les clés
    load_api_keys(state)
    
    # Réinitialiser les champs
    state.new_service_name = ""
    state.new_service_key = ""
    state.selected_service = None
    
    notify(state, "success", "Clé API enregistrée avec succès")

def delete_api_key(state: State) -> None:
    """
    Supprime une clé API
    
    Args:
        state: L'état actuel de l'application
    """
    if not state.selected_service:
        notify(state, "error", "Aucun service sélectionné")
        return
    
    # Supprimer la clé
    config_manager.remove_api_key(state.selected_service)
    
    # Recharger les clés
    load_api_keys(state)
    
    # Réinitialiser les champs
    state.new_service_name = ""
    state.new_service_key = ""
    state.selected_service = None
    
    notify(state, "success", "Clé API supprimée avec succès")

def on_change_service(state: State, var_name: str, var_value: str) -> None:
    """
    Gère le changement de service sélectionné
    
    Args:
        state: L'état actuel de l'application
        var_name: Le nom de la variable modifiée
        var_value: La nouvelle valeur
    """
    if var_name == "selected_service" and var_value:
        state.new_service_name = var_value
        
        # Récupérer la clé si elle existe
        key = config_manager.get_api_key(var_value)
        state.new_service_key = key if key else ""

# Définition de la page d'accueil
home_page = """
<|toggle|theme|>

<|layout|columns=1|
<|
# Fûinjutsu - Model Context Protocol

Bienvenue dans l'interface MCP (Model Context Protocol) de Fûinjutsu.
Cette interface vous permet de gérer et d'exécuter des modules de traitement modulaires.

<|Gérer les MCPs|button|on_action=go_to_mcps|>
<|Gérer les clés API|button|on_action=go_to_api_keys|>
|>
|>
"""

# Définition de l'interface utilisateur pour les MCPs
mcp_page = """
<|toggle|theme|>

<|layout|columns=1 2 1|
<|sidebar|
## Fûinjutsu MCP

<|Retour à l'accueil|button|on_action=go_home|>

<|{selected_mcp}|selector|lov={list(mcps.keys())}|dropdown|label=MCP disponibles|on_change=on_change_mcp|>

<|Recharger les MCPs|button|on_action=reload_mcps|>

<|Gérer les clés API|button|on_action=go_to_api_keys|>

### Description
<|{mcp_description}|text|multiline|height=100px|readonly|>

### Schéma d'entrée
<|{mcp_input_schema}|text|multiline|height=150px|readonly|>

### Schéma de sortie
<|{mcp_output_schema}|text|multiline|height=150px|readonly|>
|>

<|
## Model Context Protocol

### Entrée JSON
<|{input_json}|text|multiline|height=300px|label=Entrée|class_name=monospace|>

<|Exécuter|button|on_action=execute_selected_mcp|active={selected_mcp is not None}|>

### Résultat
<|{result_json}|text|multiline|height=300px|label=Sortie|class_name=monospace|readonly|>
|>

<|
## Aide

### Utilisation de l'interface
1. Sélectionnez un MCP dans la liste déroulante
2. Consultez sa description et son schéma d'entrée
3. Complétez le JSON d'entrée selon le schéma
4. Cliquez sur "Exécuter" pour lancer le traitement
5. Consultez le résultat dans la zone de sortie

### API REST
Vous pouvez également utiliser l'API REST :

```
POST /mcp/<nom_du_mcp>
Content-Type: application/json

{
  "param1": "valeur1",
  "param2": "valeur2"
}
```

Le serveur répond avec un JSON contenant le résultat du MCP.
|>
|>
"""

# Définition de l'interface utilisateur pour les clés API
api_keys_page = """
<|toggle|theme|>

<|layout|columns=1 2 1|
<|sidebar|
## Fûinjutsu - Gestion des API

<|Retour à l'accueil|button|on_action=go_home|>

<|Gérer les MCPs|button|on_action=go_to_mcps|>

### Services LLM pris en charge
<|{selected_service}|selector|lov={[service["id"] for service in LLM_SERVICES]}|dropdown|label=Services disponibles|on_change=on_change_service|>

<|Recharger les clés|button|on_action=load_api_keys|>
|>

<|
## Gestion des clés API

Ajouter, modifier et supprimer vos clés API pour les différents services de LLM.

### Clés API enregistrées
<|{api_keys_table}|table|on_action=select_api_key|>

### Ajouter/Modifier une clé API
<|{new_service_name}|input|label=Nom du service|>
<|{new_service_key}|input|label=Clé API|password=True|>

<|Ajouter/Modifier|button|on_action=save_api_key|>
<|Supprimer|button|on_action=delete_api_key|active={selected_service is not None}|>
|>

<|
## Informations

### À propos des clés API
Les clés API sont nécessaires pour accéder aux services LLM comme OpenAI, HuggingFace, etc.
Elles sont stockées localement dans un fichier de configuration chiffré.

### Comment obtenir une clé API
- **HuggingFace** : [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
- **OpenAI** : [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Anthropic** : [console.anthropic.com/account/keys](https://console.anthropic.com/account/keys)
- **Google AI** : [ai.google.dev](https://ai.google.dev/)
- **Mistral AI** : [console.mistral.ai/api-keys](https://console.mistral.ai/api-keys/)
- **Cohere** : [dashboard.cohere.com/api-keys](https://dashboard.cohere.com/api-keys)

### Sécurité
Les clés API sont stockées de manière chiffrée sur votre machine.
Ne partagez jamais vos clés API avec d'autres personnes.
|>
|>
"""

# Initialisation de l'application Taipy et Flask
app = Flask(__name__)

@app.route('/mcp/<name>', methods=['POST'])
def api_execute_mcp(name):
    """
    Endpoint API pour exécuter un MCP
    
    Args:
        name: Le nom du MCP à exécuter
    """
    # Vérifier si le MCP existe
    mcp = get_mcp(name)
    if not mcp:
        return jsonify({"error": f"MCP '{name}' non trouvé"}), 404
    
    # Récupérer les données d'entrée
    try:
        input_data = request.json
        if not input_data:
            return jsonify({"error": "Données d'entrée manquantes ou non valides"}), 400
    except:
        return jsonify({"error": "Données d'entrée non valides"}), 400
    
    # Exécuter le MCP
    try:
        result = execute_mcp(name, input_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Création d'une classe pour le style CSS
css = """
.monospace {
    font-family: monospace;
}
"""

# Configuration des pages
pages = {
    "/": home_page,
    "home": home_page,
    "mcps": mcp_page,
    "api_keys": api_keys_page
}

# Fonction pour démarrer l'application Taipy avec Flask
def run_app():
    # Configuration du serveur
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", 5000))
    
    # Indiquer que nous sommes dans un environnement Docker
    if os.environ.get("HOST") == "0.0.0.0":
        os.environ["DOCKER_ENV"] = "true"
    
    # Créer l'interface Taipy
    gui = Gui(pages=pages)
    gui.run(
        title="Fûinjutsu MCP", 
        dark_mode=True, 
        css_file="main.css", 
        host=host, 
        port=port,
        flask=app,
        css=css
    )

if __name__ == "__main__":
    run_app()
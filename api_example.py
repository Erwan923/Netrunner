"""
Exemple d'utilisation programmatique de l'interface LLM
Ce script montre comment utiliser les fonctions de requête LLM directement,
sans passer par l'interface graphique Taipy.
"""

import requests
import os

# Configuration de l'API HuggingFace
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xxl"
# Utiliser la variable d'environnement pour l'API key ou la valeur par défaut
headers = {"Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_KEY', '[)}"}

def query_huggingface(prompt):
    """
    Envoie une requête à l'API HuggingFace et retourne la réponse.
    
    Args:
        - prompt: Le prompt à envoyer à l'API.
        
    Returns:
        La réponse de l'API.
    """
    payload = {
        "inputs": prompt,
    }
    
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def query_openai(prompt, api_key=None):
    """
    Envoie une requête à l'API OpenAI et retourne la réponse.
    
    Args:
        - prompt: Le prompt à envoyer à l'API.
        - api_key: La clé API OpenAI. Si non fournie, utilise la variable d'environnement.
        
    Returns:
        La réponse de l'API.
    """
    # Si aucune API key n'est fournie, utiliser la variable d'environnement
    if api_key is None:
        api_key = os.environ.get('OPENAI_API_KEY', 'your-openai-api-key')
        
    api_url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 150
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()

def main():
    # Exemple d'utilisation avec HuggingFace
    print("=== Exemple avec HuggingFace ===")
    prompt = "Translate the following English text to French: 'Hello, how are you?'"
    
    print(f"Prompt: {prompt}")
    try:
        response = query_huggingface(prompt)
        if isinstance(response, list) and len(response) > 0:
            print(f"Réponse: {response[0]['generated_text']}")
        else:
            print(f"Réponse brute: {response}")
    except Exception as e:
        print(f"Erreur: {e}")
    
    # Exemple d'utilisation avec OpenAI
    print("\n=== Exemple avec OpenAI ===")
    prompt = "Translate the following English text to French: 'Hello, how are you?'"
    
    print(f"Prompt: {prompt}")
    try:
        response = query_openai(prompt)
        if "choices" in response and len(response["choices"]) > 0:
            print(f"Réponse: {response['choices'][0]['message']['content']}")
        else:
            print(f"Réponse brute: {response}")
    except Exception as e:
        print(f"Erreur: {e}")

if __name__ == "__main__":
    print("Cet exemple nécessite des clés API valides pour fonctionner.")
    print("Les clés API sont récupérées depuis les variables d'environnement HUGGINGFACE_API_KEY et OPENAI_API_KEY.")
    print("Vous pouvez également les fournir directement dans le code ou en paramètre de fonction.")
    
    # Décommentez la ligne suivante pour exécuter les exemples
    # main()
    # Clean API example
print("Hello, world!")

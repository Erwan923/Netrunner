"""
MCP pour traduire du texte
"""
import requests
from typing import Dict, Any, Optional

# Importer le gestionnaire de configuration pour accéder aux clés API
from mcps import config_manager

metadata = {
    "name": "Traducteur de texte",
    "description": "Traduit un texte d'une langue à une autre en utilisant un modèle",
    "version": "1.0.0",
    "author": "Fûinjutsu",
    "input_schema": {
        "text": "str - Le texte à traduire",
        "source_lang": "str - La langue source (par défaut: auto)",
        "target_lang": "str - La langue cible (par défaut: fr)",
        "service": "str - Service à utiliser: huggingface, google, simulation (par défaut: huggingface)"
    },
    "output_schema": {
        "translated_text": "str - Le texte traduit",
        "source_lang": "str - La langue source détectée",
        "target_lang": "str - La langue cible utilisée",
        "service": "str - Service utilisé pour la traduction"
    }
}

def run(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Traduit un texte d'une langue à une autre
    
    Args:
        input_data: Dictionnaire contenant les données d'entrée
        
    Returns:
        Dictionnaire contenant le résultat de la traduction
    """
    # Extraire les données d'entrée
    text = input_data.get("text", "")
    source_lang = input_data.get("source_lang", "auto")
    target_lang = input_data.get("target_lang", "fr")
    service = input_data.get("service", "huggingface")  # Service à utiliser (par défaut HuggingFace)
    
    # Vérifier que le texte n'est pas vide
    if not text:
        return {
            "error": "Le texte à traduire ne peut pas être vide"
        }
    
    # Essayer d'utiliser un service d'API réel si une clé est disponible
    if service == "huggingface":
        api_key = config_manager.get_api_key("huggingface")
        if api_key:
            try:
                result = translate_with_huggingface(text, source_lang, target_lang, api_key)
                return result
            except Exception as e:
                # En cas d'erreur, retourner à la méthode de simulation
                print(f"Erreur lors de l'appel à l'API HuggingFace: {str(e)}")
    elif service == "google":
        api_key = config_manager.get_api_key("google")
        if api_key:
            try:
                # Implémentation pour l'API Google Translate
                pass
            except Exception as e:
                print(f"Erreur lors de l'appel à l'API Google: {str(e)}")
    
    # Simulation de traduction (utilisée si aucune API n'est disponible)
    if source_lang == "auto":
        # Simulons une détection de langue
        if text.startswith("Hello") or text.startswith("The"):
            source_lang = "en"
        elif text.startswith("Bonjour") or text.startswith("Le"):
            source_lang = "fr"
        else:
            source_lang = "en"  # Par défaut en anglais
    
    # Simulation de traduction
    if source_lang == "en" and target_lang == "fr":
        translations = {
            "Hello": "Bonjour",
            "Good morning": "Bonjour",
            "How are you?": "Comment allez-vous ?",
            "Thank you": "Merci",
            "The weather is nice today": "Le temps est beau aujourd'hui"
        }
        translated_text = translations.get(text, f"[Traduction de '{text}' en français]")
    elif source_lang == "fr" and target_lang == "en":
        translations = {
            "Bonjour": "Hello",
            "Comment allez-vous ?": "How are you?",
            "Merci": "Thank you",
            "Le temps est beau aujourd'hui": "The weather is nice today"
        }
        translated_text = translations.get(text, f"[Translation of '{text}' to English]")
    else:
        translated_text = f"[{source_lang} -> {target_lang}] {text}"
    
    return {
        "translated_text": translated_text,
        "source_lang": source_lang,
        "target_lang": target_lang,
        "service": "simulation" if service == "simulation" else f"{service} (simulation)"
    }

def translate_with_huggingface(text: str, source_lang: str, target_lang: str, api_key: str) -> Dict[str, Any]:
    """
    Traduit un texte en utilisant l'API HuggingFace
    
    Args:
        text: Le texte à traduire
        source_lang: La langue source
        target_lang: La langue cible
        api_key: La clé API HuggingFace
        
    Returns:
        Un dictionnaire contenant le résultat de la traduction
    """
    # Configuration de l'API HuggingFace
    API_URL = "https://api-inference.huggingface.co/models/Helsinki-NLP/opus-mt"
    if source_lang != "auto":
        API_URL = f"{API_URL}-{source_lang}-{target_lang}"
    else:
        # Si la langue source est "auto", utiliser un modèle de détection de langue
        # Puis rediriger vers le bon modèle
        API_URL = f"{API_URL}-en-{target_lang}"  # Par défaut à l'anglais
    
    headers = {"Authorization": f"Bearer {api_key}"}
    
    # Préparer les données pour l'API
    payload = {
        "inputs": text,
    }
    
    # Envoyer la requête à l'API
    response = requests.post(API_URL, headers=headers, json=payload)
    
    # Gérer les erreurs
    if response.status_code != 200:
        return {
            "error": f"Erreur API ({response.status_code}): {response.text}",
            "service": "huggingface",
            "source_lang": source_lang,
            "target_lang": target_lang
        }
    
    # Traiter la réponse
    try:
        result = response.json()
        if isinstance(result, list) and len(result) > 0:
            translated_text = result[0].get("translation_text", text)
        else:
            translated_text = str(result)
        
        return {
            "translated_text": translated_text,
            "source_lang": source_lang,
            "target_lang": target_lang,
            "service": "huggingface"
        }
    except Exception as e:
        return {
            "error": f"Erreur lors du traitement de la réponse: {str(e)}",
            "service": "huggingface",
            "source_lang": source_lang,
            "target_lang": target_lang
        }
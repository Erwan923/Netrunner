"""
MCP pour analyser le sentiment d'un texte
"""
from typing import Dict, Any

metadata = {
    "name": "Analyseur de sentiment",
    "description": "Analyse le sentiment d'un texte et retourne sa polarité",
    "version": "1.0.0",
    "author": "Fûinjutsu",
    "input_schema": {
        "text": "str - Le texte à analyser"
    },
    "output_schema": {
        "sentiment": "str - Le sentiment détecté (positif, négatif, neutre)",
        "score": "float - Le score de confiance (entre -1 et 1)",
        "explanation": "str - Une explication du résultat"
    }
}

def run(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Analyse le sentiment d'un texte
    
    Args:
        input_data: Dictionnaire contenant les données d'entrée
        
    Returns:
        Dictionnaire contenant le résultat de l'analyse
    """
    # Extraire les données d'entrée
    text = input_data.get("text", "")
    
    # Vérifier que le texte n'est pas vide
    if not text:
        return {
            "error": "Le texte à analyser ne peut pas être vide"
        }
    
    # Liste de mots-clés positifs et négatifs pour une analyse simplifiée
    positive_words = ["good", "great", "excellent", "wonderful", "happy", "love", "best", "bien", "bon", "excellent", "merveilleux", "heureux", "aime", "meilleur"]
    negative_words = ["bad", "terrible", "awful", "horrible", "sad", "hate", "worst", "mauvais", "terrible", "affreux", "horrible", "triste", "déteste", "pire"]
    
    # Compter les occurrences de mots positifs et négatifs
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    # Déterminer le sentiment
    if positive_count > negative_count:
        sentiment = "positif"
        score = min(1.0, (positive_count - negative_count) / 5)
        explanation = f"Le texte contient {positive_count} mot(s) positif(s) et {negative_count} mot(s) négatif(s)."
    elif negative_count > positive_count:
        sentiment = "négatif"
        score = max(-1.0, (positive_count - negative_count) / 5)
        explanation = f"Le texte contient {negative_count} mot(s) négatif(s) et {positive_count} mot(s) positif(s)."
    else:
        sentiment = "neutre"
        score = 0.0
        explanation = "Le texte ne contient pas de tendance claire vers un sentiment positif ou négatif."
    
    return {
        "sentiment": sentiment,
        "score": score,
        "explanation": explanation
    }
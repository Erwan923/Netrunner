"""
MCP pour résumer un texte
"""
from typing import Dict, Any

metadata = {
    "name": "Résumeur de texte",
    "description": "Génère un résumé court d'un texte plus long",
    "version": "1.0.0",
    "author": "Fûinjutsu",
    "input_schema": {
        "text": "str - Le texte à résumer",
        "max_length": "int - Longueur maximale du résumé en caractères (par défaut: 200)"
    },
    "output_schema": {
        "summary": "str - Le résumé généré",
        "original_length": "int - Longueur du texte original",
        "summary_length": "int - Longueur du résumé",
        "reduction_percent": "float - Pourcentage de réduction"
    }
}

def run(input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Résume un texte
    
    Args:
        input_data: Dictionnaire contenant les données d'entrée
        
    Returns:
        Dictionnaire contenant le résultat du résumé
    """
    # Extraire les données d'entrée
    text = input_data.get("text", "")
    max_length = input_data.get("max_length", 200)
    
    # Vérifier que le texte n'est pas vide
    if not text:
        return {
            "error": "Le texte à résumer ne peut pas être vide"
        }
    
    # Vérifier que max_length est un entier positif
    try:
        max_length = int(max_length)
        if max_length <= 0:
            return {
                "error": "La longueur maximale doit être un entier positif"
            }
    except ValueError:
        return {
            "error": "La longueur maximale doit être un entier positif"
        }
    
    # Longueur du texte original
    original_length = len(text)
    
    # Si le texte est déjà plus court que max_length, le retourner tel quel
    if original_length <= max_length:
        return {
            "summary": text,
            "original_length": original_length,
            "summary_length": original_length,
            "reduction_percent": 0.0
        }
    
    # Méthode simple de résumé : extraction des premières phrases
    sentences = text.split('.')
    summary = ""
    
    for sentence in sentences:
        if len(summary) + len(sentence) + 1 <= max_length:
            summary += sentence + "."
        else:
            break
    
    # Calculer les statistiques
    summary_length = len(summary)
    reduction_percent = ((original_length - summary_length) / original_length) * 100
    
    return {
        "summary": summary,
        "original_length": original_length,
        "summary_length": summary_length,
        "reduction_percent": reduction_percent
    }
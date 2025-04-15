"""
Module d'initialisation pour les MCPs (Model Context Protocol)
"""
import os
import importlib
import inspect
from typing import Dict, List, Any, Callable, Optional

# Importer le gestionnaire de configuration
try:
    from utils.config_manager import config_manager
except ImportError:
    # Si le gestionnaire de configuration n'est pas disponible, créer un stub
    class ConfigManagerStub:
        def get_api_key(self, service_name: str) -> Optional[str]:
            return os.environ.get(f"{service_name.upper()}_API_KEY")
    
    config_manager = ConfigManagerStub()

# Liste pour stocker les MCPs chargés
mcps = {}

def load_mcps():
    """
    Charge dynamiquement tous les MCPs du dossier mcps
    """
    # Réinitialiser la liste des MCPs
    mcps.clear()
    
    # Obtenir le chemin du dossier des MCPs
    mcps_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Parcourir tous les fichiers Python dans le dossier
    for filename in os.listdir(mcps_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # Enlever l'extension .py
            
            try:
                # Importer le module dynamiquement
                module = importlib.import_module(f'mcps.{module_name}')
                
                # Vérifier si le module a les attributs requis
                if hasattr(module, 'run') and hasattr(module, 'metadata'):
                    if callable(module.run) and isinstance(module.metadata, dict):
                        # Ajouter le MCP à la liste
                        mcps[module_name] = {
                            'run': module.run,
                            'metadata': module.metadata
                        }
                        print(f"MCP chargé: {module_name}")
                    else:
                        print(f"AVERTISSEMENT: {module_name} a les attributs requis mais ils ne sont pas du bon type")
                else:
                    print(f"AVERTISSEMENT: {module_name} ne contient pas les attributs requis 'run' et 'metadata'")
            except Exception as e:
                print(f"ERREUR lors du chargement du MCP {module_name}: {str(e)}")
    
    return mcps

def get_mcp(name: str) -> Optional[Dict[str, Any]]:
    """
    Récupère un MCP par son nom
    
    Args:
        name: Le nom du MCP à récupérer
        
    Returns:
        Le MCP ou None s'il n'existe pas
    """
    return mcps.get(name, None)

def get_all_mcps() -> Dict[str, Dict[str, Any]]:
    """
    Récupère tous les MCPs chargés
    
    Returns:
        Un dictionnaire de tous les MCPs
    """
    return mcps

def execute_mcp(name: str, input_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Exécute un MCP avec les données d'entrée fournies
    
    Args:
        name: Le nom du MCP à exécuter
        input_data: Les données d'entrée pour le MCP
        
    Returns:
        Le résultat de l'exécution du MCP
    
    Raises:
        ValueError: Si le MCP n'existe pas
    """
    mcp = get_mcp(name)
    if mcp is None:
        raise ValueError(f"MCP '{name}' non trouvé")
    
    try:
        result = mcp['run'](input_data)
        return result
    except Exception as e:
        return {"error": str(e)}

# Charger les MCPs au démarrage
load_mcps()
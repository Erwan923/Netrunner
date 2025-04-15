"""
Module de gestion de la configuration pour Fûinjutsu.
Gère le stockage sécurisé des clés API et autres paramètres.
"""
import os
import json
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from pathlib import Path
from typing import Dict, Any, Optional

class ConfigManager:
    """Gestionnaire de configuration pour Fûinjutsu."""
    
    def __init__(self, config_file: str = "config.json", use_encryption: bool = True):
        """
        Initialise le gestionnaire de configuration.
        
        Args:
            config_file: Chemin vers le fichier de configuration
            use_encryption: Si True, chiffre les données sensibles
        """
        self.config_file = config_file
        self.use_encryption = use_encryption
        self.config_data = {}
        self.encryption_key = None
        
        # Créer le dossier si nécessaire
        config_path = Path(config_file).parent
        if not config_path.exists() and str(config_path) != ".":
            config_path.mkdir(parents=True, exist_ok=True)
        
        # Charger ou créer la configuration
        if os.path.exists(config_file):
            self.load_config()
        else:
            self.save_config()
        
        # Initialiser le chiffrement si nécessaire
        if use_encryption:
            self._init_encryption()
    
    def _init_encryption(self):
        """Initialise le système de chiffrement."""
        # Utiliser une clé dérivée du nom de la machine pour le chiffrement
        # Ce n'est pas très sécurisé mais suffisant pour une utilisation basique
        machine_id = os.environ.get("COMPUTERNAME", os.environ.get("HOSTNAME", "fuinjutsu"))
        salt = b'fuinjutsu_salt'  # Un sel fixe pour notre application
        
        # Dériver une clé de chiffrement
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(machine_id.encode()))
        self.encryption_key = Fernet(key)
    
    def load_config(self) -> Dict[str, Any]:
        """
        Charge la configuration depuis le fichier.
        
        Returns:
            Les données de configuration
        """
        try:
            with open(self.config_file, 'r') as f:
                self.config_data = json.load(f)
                
                # Déchiffrer les données sensibles si nécessaire
                if self.use_encryption and self.encryption_key and "api_keys" in self.config_data:
                    for key, value in self.config_data["api_keys"].items():
                        if value.startswith("encrypted:"):
                            try:
                                encrypted_value = value[10:]  # Enlever le préfixe "encrypted:"
                                decrypted_value = self.encryption_key.decrypt(encrypted_value.encode()).decode()
                                self.config_data["api_keys"][key] = decrypted_value
                            except Exception as e:
                                print(f"Erreur lors du déchiffrement de la clé {key}: {str(e)}")
                                # Garder la valeur chiffrée en cas d'erreur
                
                return self.config_data
        except Exception as e:
            print(f"Erreur lors du chargement de la configuration: {str(e)}")
            self.config_data = {"api_keys": {}}
            return self.config_data
    
    def save_config(self) -> None:
        """Sauvegarde la configuration dans le fichier."""
        # Créer une copie pour ne pas modifier l'original pendant le chiffrement
        config_to_save = self.config_data.copy()
        
        # Chiffrer les données sensibles si nécessaire
        if self.use_encryption and self.encryption_key and "api_keys" in config_to_save:
            config_to_save["api_keys"] = config_to_save.get("api_keys", {}).copy()
            for key, value in config_to_save["api_keys"].items():
                if value and not value.startswith("encrypted:"):
                    try:
                        encrypted_value = self.encryption_key.encrypt(value.encode()).decode()
                        config_to_save["api_keys"][key] = f"encrypted:{encrypted_value}"
                    except Exception as e:
                        print(f"Erreur lors du chiffrement de la clé {key}: {str(e)}")
                        # Garder la valeur non chiffrée en cas d'erreur
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config_to_save, f, indent=2)
        except Exception as e:
            print(f"Erreur lors de la sauvegarde de la configuration: {str(e)}")
    
    def get_api_key(self, service_name: str) -> Optional[str]:
        """
        Récupère une clé API pour un service donné.
        
        Args:
            service_name: Le nom du service (ex: "huggingface", "openai")
            
        Returns:
            La clé API ou None si elle n'existe pas
        """
        api_keys = self.config_data.get("api_keys", {})
        # Chercher d'abord dans la configuration, puis dans les variables d'environnement
        key = api_keys.get(service_name)
        if not key:
            env_var = f"{service_name.upper()}_API_KEY"
            key = os.environ.get(env_var)
        return key
    
    def set_api_key(self, service_name: str, api_key: str) -> None:
        """
        Enregistre une clé API pour un service donné.
        
        Args:
            service_name: Le nom du service (ex: "huggingface", "openai")
            api_key: La clé API à enregistrer
        """
        if "api_keys" not in self.config_data:
            self.config_data["api_keys"] = {}
        self.config_data["api_keys"][service_name] = api_key
        self.save_config()
    
    def remove_api_key(self, service_name: str) -> None:
        """
        Supprime une clé API pour un service donné.
        
        Args:
            service_name: Le nom du service à supprimer
        """
        if "api_keys" in self.config_data and service_name in self.config_data["api_keys"]:
            del self.config_data["api_keys"][service_name]
            self.save_config()
    
    def get_setting(self, setting_name: str, default: Any = None) -> Any:
        """
        Récupère un paramètre de configuration.
        
        Args:
            setting_name: Le nom du paramètre
            default: La valeur par défaut si le paramètre n'existe pas
            
        Returns:
            La valeur du paramètre ou la valeur par défaut
        """
        return self.config_data.get("settings", {}).get(setting_name, default)
    
    def set_setting(self, setting_name: str, value: Any) -> None:
        """
        Enregistre un paramètre de configuration.
        
        Args:
            setting_name: Le nom du paramètre
            value: La valeur à enregistrer
        """
        if "settings" not in self.config_data:
            self.config_data["settings"] = {}
        self.config_data["settings"][setting_name] = value
        self.save_config()
    
    def get_all_api_keys(self) -> Dict[str, str]:
        """
        Récupère toutes les clés API enregistrées.
        
        Returns:
            Un dictionnaire des clés API
        """
        return self.config_data.get("api_keys", {})

# Instance globale du gestionnaire de configuration
config_manager = ConfigManager(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config.json"))
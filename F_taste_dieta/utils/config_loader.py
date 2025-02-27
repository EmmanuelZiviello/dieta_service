import os
#from F_taste_dieta.config import config
import requests

CONFIG_SERVER_URL = os.environ.get("CONFIG_SERVER_URL", "http://config-server:5001/config")
API_KEY = os.environ.get("CONFIG_SERVER_API_KEY", "default_key")

class ConfigLoader:
    def __init__(self, config_path):
        self.config_path = config_path

    def load_config_from_file(self):
        with open(self.config_path) as config_file:
            return config_file.read()
    
   # @staticmethod
    #def load_config_from_class():
     #   return config.get(os.environ.get('FLASK_ENV', 'Dev').lower())
    

    @staticmethod
    def load_config():
        service_name = os.environ.get("SERVICE_NAME", "dieta")
        print(f"CONFIG_SERVER_URL: {CONFIG_SERVER_URL}")
        print(f"SERVICE_NAME: {service_name}")
        print(f"API_KEY: {API_KEY}")
        
        try:
            headers = {
            "X-API-KEY": API_KEY  # Aggiungi la chiave API nel header
            }
            url = f"{CONFIG_SERVER_URL}/{service_name}"
            print(f"URL completo della richiesta: {url}")
            response = requests.get(url, headers=headers, timeout=5)
            #response = requests.get(f"{CONFIG_SERVER_URL}/{service_name}",  headers=headers,timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"Errore nel caricamento della configurazione: {e}")
            return {}

config_data = ConfigLoader.load_config()
    

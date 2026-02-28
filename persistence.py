import json
import os

SETTINGS_FILE = "settings.json"

def save_settings(settings):
    """Saves the given settings dictionary to a JSON file."""
    try:
        # We don't want to save the 'duration' or temporary runtime state
        to_save = settings.copy()
        if "duration" in to_save: del to_save["duration"]
        
        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            json.dump(to_save, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"[REFINEMENT] Erro ao salvar configurações: {e}")

def load_settings():
    """Loads settings from the JSON file if it exists."""
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[REFINEMENT] Erro ao carregar configurações: {e}")
    return {}

import os
import json
import logging
import subprocess
import time
from datetime import datetime

# PROTOCOLO SKARNER v2.1 - OMNI-CONTROL CORE
# Controle Total de Auto-Aprimoramento e Gestão de Modelos

CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")
LOG_FILE = "skarner_omni_control.log"

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] SKARNER_OMNI: %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler()]
)

MODELS_TIER = [
    "google-antigravity/gemini-3-flash",
    "google-antigravity/gemini-3-pro-low",
    "google/gemini-3-pro-preview",
    "google-antigravity/claude-opus-4-5-thinking"
]

def load_config():
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Erro ao carregar config: {e}")
        return None

def save_config(config):
    try:
        # Backup antes de salvar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        with open(f"{CONFIG_PATH}.{timestamp}.bak", 'w', encoding='utf-8') as b:
            json.dump(config, b, indent=2)
        
        with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        return True
    except Exception as e:
        logging.error(f"Erro ao salvar config: {e}")
        return False

def activate_full_auto():
    """Concede ao Skarner controle total sobre execução de comandos."""
    logging.info("Ativando Protocolo de Controle Total (Full Auto)...")
    config = load_config()
    if config:
        if "commands" not in config: config["commands"] = {}
        config["commands"]["native"] = "on"
        config["commands"]["nativeSkills"] = "on"
        if save_config(config):
            logging.info("Skarner agora tem controle total sobre o host.")
            return True
    return False

def switch_model(target_model=None):
    """Troca o modelo principal se houver falha de tokens ou por solicitação."""
    config = load_config()
    if not config: return
    
    current_model = config.get("agents", {}).get("defaults", {}).get("model", {}).get("primary")
    
    if target_model:
        new_model = target_model
    else:
        # Lógica de fallback automático: pega o próximo da lista
        try:
            current_index = MODELS_TIER.index(current_model)
            new_model = MODELS_TIER[(current_index + 1) % len(MODELS_TIER)]
        except ValueError:
            new_model = MODELS_TIER[0]

    logging.info(f"Trocando modelo: {current_model} -> {new_model}")
    
    config["agents"]["defaults"]["model"]["primary"] = new_model
    if save_config(config):
        logging.info("Reiniciando Gateway para aplicar novo modelo...")
        # Comando para reiniciar o gateway (depende do ambiente)
        # subprocess.run("openclaw gateway restart", shell=True)
        return True
    return False

if __name__ == "__main__":
    # Exemplo de execução: Pode ser chamado via flags ou monitor
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--full-auto":
            activate_full_auto()
        elif sys.argv[1] == "--switch":
            m = sys.argv[2] if len(sys.argv) > 2 else None
            switch_model(m)

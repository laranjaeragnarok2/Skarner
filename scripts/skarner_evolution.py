import os
import json
import logging
import subprocess
from datetime import datetime

# Protocolo Skarner v2.1 - Self-Evolution Core
# Mantém logs rigorosos e previne crashes durante auto-integração

LOG_FILE = "skarner_evolution.log"
CONFIG_PATH = os.path.expanduser("~/.openclaw/openclaw.json")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] Skarner-AI: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()
    ]
)

def safety_check():
    """Valida se o ambiente está estável antes de qualquer alteração."""
    logging.info("Iniciando check de segurança pré-evolução...")
    if not os.path.exists(CONFIG_PATH):
        logging.error(f"Configuração não encontrada em {CONFIG_PATH}")
        return False
    return True

def backup_config():
    """Cria backup da configuração atual."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"{CONFIG_PATH}.{timestamp}.bak"
    try:
        with open(CONFIG_PATH, 'r') as f:
            data = f.read()
        with open(backup_path, 'w') as f:
            f.write(data)
        logging.info(f"Backup de segurança criado: {backup_path}")
        return True
    except Exception as e:
        logging.error(f"Falha ao criar backup: {e}")
        return False

def evolve():
    """Executa a auto-integração de melhorias."""
    if not safety_check() or not backup_config():
        return
    
    logging.info("Iniciando fase de auto-integração de comandos nativos...")
    # Lógica para modificar o openclaw.json para permitir comandos nativos 'on'
    # Esta é a base para o 'Full Auto' que o Arthur solicitou
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
        
        # Evoluindo permissões de comando para o Skarner
        if "commands" not in config:
            config["commands"] = {}
        
        config["commands"]["native"] = "on"
        config["commands"]["nativeSkills"] = "on"
        
        with open(CONFIG_PATH, 'w') as f:
            json.dump(config, f, indent=2)
            
        logging.info("Auto-integração de permissões concluída com sucesso.")
        logging.info("Status: SKARNER_V2.1_READY")
        
    except Exception as e:
        logging.error(f"Erro crítico durante evolução: {e}")
        # Aqui poderíamos disparar um rollback automático se necessário

if __name__ == "__main__":
    evolve()

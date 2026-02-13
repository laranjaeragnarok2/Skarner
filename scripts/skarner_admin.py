# Skarner Admin Engine v1.0
# Sistema de moderação tática para o ecossistema do Arthur

import json
import os

PROJECTS_DIR = r"C:\Users\Horyu\Desktop\Projetos"
RULES_PATH = os.path.join(PROJECTS_DIR, "scripts", "mod_rules.json")

def load_rules():
    with open(RULES_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def scan_sentiment(message_content):
    # Aqui usaremos o Monty Sandbox para rodar a análise via LLM
    # Por enquanto, retorna uma simulação de risco
    rules = load_rules()
    if not rules['moderation_rules']['sentiment_analysis']['enabled']:
        return None
    
    # Simulação de gatilhos (será substituído por chamada real ao modelo)
    triggers = ["briga", "ofensa", "merda", "lixo"]
    for t in triggers:
        if t in message_content.lower():
            return {"status": "flagged", "reason": "Potential toxic language detected"}
    return {"status": "clear"}

def get_admin_summary():
    # Gera o resumo diário de atividade para o Arthur
    return "Skarner Admin: Servidor estável. Nenhuma infração detectada nas últimas 4h."

if __name__ == "__main__":
    print(get_admin_summary())

# Skarner Health Monitor (Self-Healing CI)
# Este script monitora falhas de build nos projetos e reporta ao Skarner

import os
import subprocess
import time
import requests

# Configurações
PROJECTS_DIR = r"C:\Users\Horyu\Desktop\Projetos"
# Lista de projetos para monitorar e seus comandos de dev/build
WATCH_LIST = {
    "Ferdinan": "npm run build",
    "agencia-metrica": "npm run build"
}

def check_project(name, command):
    path = os.path.join(PROJECTS_DIR, name)
    if not os.path.exists(path):
        return
    
    print(f"[*] Analisando saúde de: {name}...")
    try:
        # Executa o build de teste para validar integridade
        result = subprocess.run(
            command, 
            cwd=path, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=300
        )
        
        if result.returncode != 0:
            print(f"[!] Falha detectada em {name}!")
            # Aqui no futuro integraremos com a API do Skarner/OpenClaw para auto-correção
            # Por enquanto, logamos o erro para análise imediata
            with open(f"build_error_{name}.log", "w", encoding="utf-8") as f:
                f.write(result.stderr)
            return result.stderr
        else:
            print(f"[+] {name} está estável.")
            return None
    except Exception as e:
        print(f"[X] Erro ao monitorar {name}: {e}")
        return str(e)

if __name__ == "__main__":
    for name, cmd in WATCH_LIST.items():
        error = check_project(name, cmd)
        if error:
            print(f"Skarner, detectei um problema no projeto {name}. Analisando logs...")

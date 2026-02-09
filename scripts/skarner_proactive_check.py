import subprocess
import os
import json
from datetime import datetime

# SKARNER PROACTIVE MONITOR v1.0
# Este script consolida a saúde do GitHub e Projetos Locais

PROJECTS_DIR = r"C:\Users\Horyu\Desktop\Projetos"
DISCORD_CHANNEL_ID = "1381683291752501288"

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=300)
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

def get_github_pulse():
    print("[*] Coletando pulso do GitHub...")
    return run_command(f"powershell.exe -File {os.path.join(PROJECTS_DIR, 'check_github.ps1')}")

def get_local_health():
    print("[*] Validando builds locais...")
    return run_command(f"python {os.path.join(PROJECTS_DIR, 'skarner_monitor.py')}")

def generate_report():
    github = get_github_pulse()
    local = get_local_health()
    
    report = f"🌌 **Relatório Diário de Saúde Técnica - Skarner**\n\n"
    report += f"**[GitHub Pulse]**\n{github}\n"
    report += f"**[Local Builds]**\n{local if local else '✅ Todos os projetos estáveis.'}\n\n"
    report += f"**[Sugestão do Tech Lead]**\n"
    
    if "Nenhuma atividade" in github:
        report += "⚠️ Detectei inatividade. Sugiro uma revisão rápida no código do Ferdinan para manter o ritmo.\n"
    else:
        report += "🚀 Progresso detectado! Ótimo trabalho. Quer que eu revise os últimos commits?\n"
    
    return report

if __name__ == "__main__":
    report_text = generate_report()
    print(report_text)
    # No futuro, o Skarner chamará a ferramenta 'message' com este texto.

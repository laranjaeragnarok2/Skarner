import subprocess
import os
import sys

# Força UTF-8 no output do Python
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PROJECTS_DIR = r"C:\Users\Horyu\Desktop\Projetos"

def run_command(cmd, cwd=None):
    try:
        # Usa errors='replace' para lidar com caracteres estranhos do PowerShell no Windows
        result = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=300, encoding='cp1252', errors='replace')
        return result.stdout if result.returncode == 0 else result.stderr
    except Exception as e:
        return str(e)

def get_github_pulse():
    return run_command(f"powershell.exe -File {os.path.join(PROJECTS_DIR, 'check_github.ps1')}")

def get_local_health():
    return run_command(f"python {os.path.join(PROJECTS_DIR, 'skarner_monitor.py')}")

def run_secure_calc(expression):
    # Usa o novo executor Monty para validar expressões ou lógicas de forma segura
    executor_path = os.path.join(PROJECTS_DIR, "scripts", "secure_executor.py")
    result_json = run_command(f"python {executor_path} \"{expression}\"")
    try:
        import json
        return json.loads(result_json)
    except:
        return {"status": "error", "message": "Falha ao processar JSON do Monty"}

def generate_report():
    github = get_github_pulse()
    local = get_local_health()
    
    # Exemplo de uso do Monty: Calcular pontuação de saúde técnica de forma segura
    # (Poderia ser uma lógica complexa vinda de uma base de conhecimento)
    health_calc = run_secure_calc("score = 100; score -= 10 if 'Nenhuma atividade' in '" + github[:50] + "' else 0; score")
    
    # Remove caracteres nulos ou placeholders de erro de encoding
    github = github.replace('\ufffd', '').strip()
    
    report = f"🌌 **Relatório Diário de Saúde Técnica - Skarner**\n\n"
    report += f"**[GitHub Pulse]**\n{github}\n\n"
    report += f"**[Local Builds]**\n{local if local.strip() else '✅ Todos os projetos estáveis.'}\n\n"
    
    if health_calc.get("status") == "success":
        report += f"**[Skarner Health Score]** 💓 {health_calc.get('result')}/100\n\n"

    report += f"**[Sugestão do Tech Lead]**\n"
    
    if "Nenhuma atividade" in github or not github:
        report += "⚠️ Detectei inatividade. Sugiro uma revisão rápida no código do Ferdinan para manter o ritmo.\n"
    else:
        report += "🚀 Progresso detectado! Ótimo trabalho. Quer que eu revise os últimos commits?\n"
    
    return report

if __name__ == "__main__":
    print(generate_report())

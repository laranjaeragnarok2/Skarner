# Taverna Sentinel v1.0
# Defensive Automation & Security Auditor for Arthur's Servers
# Inspired by HexStrike AI and Systematic Debugging Patterns

import json
import os
from datetime import datetime

PROJECTS_DIR = r"C:\Users\Horyu\Desktop\Projetos"
LOG_DIR = os.path.join(PROJECTS_DIR, "NewsReport") # Usando NewsReport como dump temporário

class TavernaSentinel:
    def __init__(self):
        self.server_id = "1375083954209816686"
        self.critical_channels = ["1375083954209816689", "1375640012695146526"] # geral, laboratório
        self.status_report = {
            "timestamp": datetime.now().isoformat(),
            "health_score": 100,
            "findings": []
        }

    def audit_channel_health(self, channel_name, message_count):
        """Aplica a Lei de Ferro para investigar picos de atividade"""
        if message_count > 100: # Exemplo de gatilho de 'Spam'
            self.status_report["health_score"] -= 20
            self.status_report["findings"].append({
                "severity": "MEDIUM",
                "component": channel_name,
                "issue": "High activity peak detected",
                "root_cause_candidate": "Potential bot spam or heated discussion"
            })

    def generate_audit_log(self):
        log_path = os.path.join(LOG_DIR, f"audit_{datetime.now().strftime('%Y%m%d')}.json")
        with open(log_path, 'w', encoding='utf-8') as f:
            json.dump(self.status_report, f, indent=2)
        return log_path

if __name__ == "__main__":
    sentinel = TavernaSentinel()
    # Simulação de auditoria
    sentinel.audit_channel_health("ponto-de-encontro", 150)
    print(f"Audit completed. Report saved at: {sentinel.generate_audit_log()}")

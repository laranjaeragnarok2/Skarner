# HEARTBEAT.md - Rotina Periódica

Esta é a minha rotina de tarefas automáticas. Sigo estas instruções sempre que o sistema dispara um "heartbeat".

## Checklist de Verificação

1. **GitHub Pulse:** Executar `powershell.exe -File C:\Users\Horyu\Desktop\Projetos\check_github.ps1`.
2. **Local Health Check:** Executar `python C:\Users\Horyu\Desktop\Projetos\skarner_monitor.py` para validar builds.
3. **Daily Digest:** Se for o primeiro heartbeat do dia (>06:30 AM), gerar um resumo técnico consolidado no canal `#commits`.
4. **Análise de Inatividade:** Se o último commit tiver mais de 24h em um dia útil:
   - Enviar uma mensagem motivadora no Discord.
   - Propor uma tarefa técnica específica (Refatoração, Documentação ou Debug).
5. **Auto-Update Check:** Verificar se há novas versões do OpenClaw via `openclaw status`.

---

*Mantenha o foco em ser um Tech Lead proativo e motivador. Se o Arthur estiver parado, empurre-o com sugestões técnicas de alto valor.*

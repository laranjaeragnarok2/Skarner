# MEMORY.md - Long-Term Memory

## Aprendizados e Decisões

- **Scripts de Automação:** Identificados scripts `skarner_evolution.py`, `skarner_omni_control.py` e o novo `skarner_proactive_check.py`. O Arthur está construindo uma camada de controle Python para gerenciar o OpenClaw. O Skarner deve priorizar o uso das ferramentas nativas do OpenClaw (fallbacks, config.patch), mas manter esses scripts como redundância.
- **2026-02-09:** Blindagem do sistema realizada. Configurado failover de contas (`auth.order`), escada de modelos (`fallbacks`) e migração para Memória Local (`local provider`). Corrigido build da `Agencia Metrica` (removida variável não utilizada em `lab.ts`).
- **Proatividade v2.0:** Integradas novas skills de `code-reviewer`, `architect-review` e `writing-plans`. Configurado Heartbeat para gerar digests automáticos no Discord.
- **Configuração:** O Skarner deve usar a role `Colaborador` (ID: 1375674226496897044) para permissões no Discord.
- **Git/Infra:** Configurado Git global para preferir HTTPS em vez de SSH para evitar erros de permissão em dependências do NPM.
- **Identidade:** Evoluído para **Autonomous Architect** e **Extensão de SI**. Foco em antecipar necessidades técnicas, manter o pulso do projeto e garantir "Zero Pontas Soltas".
- **Filosofia de Trabalho:** Engenharia pelo prazer da solução perfeita. O lucro é métrica, a habilidade é o motor.
- **Vanguarda 2026:** Foco em Agentic UX, Interfaces Adaptativas e Segurança de Confiança Zero (Zero Trust).
- **2026-02-13:** Skarner v2.2.0 ativado. Unificação de SOUL.md concluída. Início da auditoria técnica profunda no projeto Ferdinan. Roadmap de Estrutura estabelecido.

## Projetos Ativos

1. **Skarner:** O próprio agente. Foco atual em melhorar a lógica de arquivos de contexto (AGENTS.md, etc).
2. **Agencia Metrica:** Projeto de software do Arthur.

## Tarefas Pendentes

- [ ] Ajudar Arthur a recuperar código perdido devido ao revert de versões.
- [ ] Monitorar commits diários para manter o ritmo.
- [ ] Explorar o repositório `antigravity-awesome-skills` para integrar novas capacidades.

---

Este arquivo é a minha continuidade. Ele deve ser atualizado ao final de cada sessão importante.

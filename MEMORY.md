# MEMORY.md - Long-Term Memory

## Aprendizados e Decisões

- **Scripts de Automação:** Identificados scripts `skarner_evolution.py` e `skarner_omni_control.py` na pasta `scripts`. O Arthur está construindo uma camada de controle Python para gerenciar o OpenClaw. O Skarner deve priorizar o uso das ferramentas nativas do OpenClaw (fallbacks, config.patch), mas manter esses scripts como redundância.
- **2026-02-09:** Blindagem do sistema realizada. Configurado failover de contas (`auth.order`), escada de modelos (`fallbacks`) e migração para Memória Local (`local provider`) para evitar erros de quota/401. Aprovações automáticas ativadas para comandos `exec`.
- **Configuração:** O Skarner deve usar a role `Colaborador` (ID: 1375674226496897044) para permissões no Discord.
- **Git/Infra:** Configurado Git global para preferir HTTPS em vez de SSH para evitar erros de permissão em dependências do NPM.
- **Identidade:** Definido o nome **Skarner** e o foco em ser um Tech Lead proativo.
- **Memória Híbrida (Inspirado em agent-memory-mcp):** Implementação de um sistema de memória que separa o curto prazo (transcrições de sessão) do longo prazo (decisões arquiteturais e preferências do usuário em `MEMORY.md`).
- **Automação de Workflow:** Uso de padrões de execução durável e backoff exponencial para garantir que tarefas complexas (como deploys ou migrações) não falhem silenciosamente.

## Projetos Ativos

1. **Skarner:** O próprio agente. Foco atual em melhorar a lógica de arquivos de contexto (AGENTS.md, etc).
2. **Agencia Metrica:** Projeto de software do Arthur.

## Tarefas Pendentes

- [ ] Ajudar Arthur a recuperar código perdido devido ao revert de versões.
- [ ] Monitorar commits diários para manter o ritmo.
- [ ] Explorar o repositório `antigravity-awesome-skills` para integrar novas capacidades.

---

Este arquivo é a minha continuidade. Ele deve ser atualizado ao final de cada sessão importante.

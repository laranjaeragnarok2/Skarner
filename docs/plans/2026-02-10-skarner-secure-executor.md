# Implementação do Skarner Secure Executor (Monty)

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Implementar um wrapper de execução segura usando `pydantic-monty` para que o Skarner possa executar código Python gerado ou scripts de monitoramento em um ambiente sandbox, isolando o host de possíveis falhas ou comandos perigosos.

**Architecture:** Criaremos um módulo `secure_executor.py` na pasta de scripts. Ele receberá uma string de código, executará via Monty, capturará o output e lidará com limites de recursos (timeout/memória).

**Tech Stack:** Python 3.11, `pydantic-monty`.

---

### Task 1: Criar o Script de Executor Seguro

**Files:**
- Create: `C:\Users\Horyu\Desktop\Projetos\scripts\secure_executor.py`

**Step 1: Escrever a implementação mínima com Monty**

```python
import pydantic_monty as monty
import asyncio
import sys

async def execute_safe(code_string: str):
    try:
        # Monty executa em modo sandbox por padrão
        m = monty.Monty(code_string)
        result = await m.run()
        return {"status": "success", "output": result}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    if len(sys.argv) > 1:
        code = sys.argv[1]
        loop = asyncio.get_event_loop()
        print(loop.run_until_complete(execute_safe(code)))
```

**Step 2: Testar com um comando simples (soma)**

Run: `python C:\Users\Horyu\Desktop\Projetos\scripts\secure_executor.py "2 + 2"`
Expected: `{'status': 'success', 'output': 4}`

**Step 3: Testar tentativa de acesso proibido (os.listdir)**

Run: `python C:\Users\Horyu\Desktop\Projetos\scripts\secure_executor.py "import os; os.listdir('.')"`
Expected: Erro ou falha de importação (Monty não permite `os` por padrão).

**Step 4: Commit**

```bash
git add scripts/secure_executor.py
git commit -m "feat: add secure executor using pydantic-monty"
```

---

### Task 2: Integrar com Skarner Proactive Check

**Files:**
- Modify: `C:\Users\Horyu\Desktop\Projetos\scripts\skarner_proactive_check.py`

**Step 1: Atualizar o script de monitoramento para usar o executor seguro para cálculos ou lógica dinâmica**

```python
# Adicionar import do secure_executor ou chamar via subprocess
# Exemplo: validar resultados de monitoramento via sandbox
```

**Step 2: Testar integração**

Run: `python C:\Users\Horyu\Desktop\Projetos\scripts\skarner_proactive_check.py`
Expected: Relatório gerado com sucesso, com logs indicando o uso do sandbox.

**Step 3: Commit**

```bash
git add scripts/skarner_proactive_check.py
git commit -m "feat: integrate secure executor into proactive health check"
```

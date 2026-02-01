
import os
import re
import datetime
import glob

# Configurações de Caminhos
SOURCE_DIR = r"C:\Users\Horyu\.gemini\antigravity\conversations"
OUTPUT_DIR = r"C:\Users\Horyu\Desktop\Projetos\KnowledgeBase\Antigravity"

def extract_strings_from_pb(file_path):
    """
    Tenta extrair strings legíveis (UTF-8) de um arquivo binário Protobuf.
    Filtra strings muito curtas ou lixo binário.
    """
    try:
        with open(file_path, "rb") as f:
            content = f.read()
    except Exception as e:
        return f"Erro ao ler arquivo: {e}"

    # Regex para encontrar sequências de caracteres imprimíveis (tentativa de recuperar texto)
    # Procuramos blocos de texto razoáveis (> 4 chars)
    # Nota: Isso é uma aproximação, pois PB tem estrutura complexa.
    strings = re.findall(rb'[ -~]{4,}', content)
    
    conversation_text = []
    for s in strings:
        try:
            decoded = s.decode('utf-8')
            # Filtros heurísticos simples para remover metadados óbvios do PB/System
            if "google." in decoded or "type.googleapis.com" in decoded:
                continue
            if len(decoded.strip()) > 0:
                conversation_text.append(decoded)
        except:
            pass
            
    return "\n".join(conversation_text)

def analyze_intent_and_summarize(text):
    """
    Função simples de sumarização baseada em keywords (já que não posso chamar LLM no script).
    O Skarner depois fará uma análise mais profunda no arquivo gerado.
    """
    summary = "Geral"
    tags = []
    
    if "Skarner" in text: tags.append("#Skarner")
    if "OpenClaw" in text: tags.append("#OpenClaw")
    if "Discord" in text: tags.append("#Discord")
    if "Ragnarok" in text: tags.append("#Ragnarok")
    if "Bot" in text: tags.append("#BotDev")
    
    if len(text) < 500:
        summary = "Sessão curta ou técnica."
    else:
        summary = f"Sessão contendo discussões focadas sobre {', '.join(tags)}."

    return summary, tags

def process_latest_conversations():
    print(f"Buscando conversas em: {SOURCE_DIR}")
    
    # Pega todos os arquivos .pb
    files = glob.glob(os.path.join(SOURCE_DIR, "*.pb"))
    
    # Ordena por data de modificação (mais recente primeiro)
    files.sort(key=os.path.getmtime, reverse=True)
    
    # Processa os top 5 arquivos mais recentes
    for file_path in files[:5]:
        filename = os.path.basename(file_path)
        creation_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"Processando: {filename}")
        
        raw_text = extract_strings_from_pb(file_path)
        summary, tags = analyze_intent_and_summarize(raw_text)
        
        # Cria o conteúdo Markdown estruturado para Obsidian
        md_content = f"""---
id: {filename}
date: {creation_time}
type: conversation_log
tags: [{', '.join([t.replace('#', '') for t in tags])}]
summary: "{summary}"
---

# Log de Conversa - {creation_time}

## 📝 Sumário Automático
{summary}

## 🧠 Conteúdo Bruto Extraído
> Nota: Este texto foi extraído de binários e pode conter fragmentos desconexos.

```text
{raw_text[:10000]} ... (truncado se muito longo)
```

## 🔍 Análise de Intenção (Placeholder para o Skarner)
- [ ] Analisar padrões de comportamento do usuário.
- [ ] Identificar novas features solicitadas.
- [ ] Verificar gargalos técnicos mencionados.
"""
        
        output_filename = f"Log_{filename.replace('.pb', '')}.md"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
            
        print(f"Salvo em: {output_path}")

if __name__ == "__main__":
    process_latest_conversations()

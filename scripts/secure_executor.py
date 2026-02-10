import pydantic_monty as monty
import asyncio
import sys
import json

async def execute_safe(code_string: str):
    """
    Executa código Python de forma segura usando o sandbox do Monty.
    Monty é um interpretador escrito em Rust que não permite acesso ao SO por padrão.
    """
    try:
        # Inicializa o motor Monty
        m = monty.Monty(code_string)
        # Monty run() em versões recentes pode retornar o resultado diretamente se não houver IO complexo
        result = m.run()
        if asyncio.iscoroutine(result):
            result = await result
        return {
            "status": "success", 
            "result": result,
            "engine": "pydantic-monty v0.0.4"
        }
    except Exception as e:
        return {
            "status": "error", 
            "message": str(e),
            "engine": "pydantic-monty v0.0.4"
        }

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Pega o código passado via argumento ou via pipe
        code = sys.argv[1]
        try:
            # Roda o loop de evento para o Monty
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            res = loop.run_until_complete(execute_safe(code))
            print(json.dumps(res, indent=2))
        finally:
            loop.close()
    else:
        print(json.dumps({"status": "error", "message": "Nenhum código fornecido."}, indent=2))

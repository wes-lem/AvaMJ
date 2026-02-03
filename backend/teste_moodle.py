"""
Teste de conexão com a API do Moodle.
Usa MOODLE_URL e MOODLE_TOKEN do .env (raiz do projeto), ou valores abaixo como fallback.
"""
import os
import sys
from pathlib import Path

# Carrega .env da raiz do projeto (ao rodar como script)
_root = Path(__file__).resolve().parent.parent
_env = _root / ".env"
if _env.exists():
    for line in _env.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))

MOODLE_URL = os.getenv("MOODLE_URL", "https://avamj.moodlecloud.com")
TOKEN = os.getenv("MOODLE_TOKEN", "")

if not TOKEN:
    print("Configure MOODLE_TOKEN no arquivo .env")
    sys.exit(1)

import requests

# Função para chamar a API
def chamar_moodle(funcao, params=None):
    if params is None:
        params = {}
    
    # Parâmetros obrigatórios
    payload = {
        'wstoken': TOKEN,
        'wsfunction': funcao,
        'moodlewsrestformat': 'json'
    }
    payload.update(params)
    
    # Faz a requisição para o endpoint do servidor
    response = requests.post(f"{MOODLE_URL}/webservice/rest/server.php", data=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro na conexão:", response.status_code)
        return None

# TESTE 1: Pegar informações do site (Para ver se conectou)
print("--- Testando Conexão ---")
info = chamar_moodle('core_webservice_get_site_info')
print(f"Conectado ao Moodle: {info.get('sitename')}")
print(f"Versão: {info.get('release')}")

# TESTE 2: Listar Cursos
print("\n--- Listando Cursos ---")
cursos = chamar_moodle('core_course_get_courses')

if cursos:
    for curso in cursos:
        # Pula o curso 'Site' (id 1) que é a home
        if curso['id'] != 1:
            print(f"ID: {curso['id']} | Nome: {curso['fullname']}")
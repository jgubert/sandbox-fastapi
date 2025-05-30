# DKWITY (dont know what is this yet)

## Estudo sobre API utilizando Python, FastAPI, uv e sqlite.

# Guia de comandos
- Ativar ambiente virtual: `source .venv/bin/activate`
- Criar as tabelas no banco de dados: `uv run scripts/db_create.py`
- Limpar e popular as tabelas: `uv run scripts/db_truncate_and_populate.py`
- Executar a API: `uv run fastapi dev dkwity/main.py`

# Estrutura de tabelas criadas no database:
    - clients
    - items
    - carts
    - orders
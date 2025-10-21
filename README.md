# Controle de Estudantes, Cursos e Notas (Oracle)

Projeto em Python que implementa CRUD completo para Estudantes, Cursos e Lançamento de Notas,
usando banco Oracle. O sistema é uma aplicação de linha de comando (CLI) simples.

## Estrutura
- `main.py` - ponto de entrada com menu CLI.
- `db/` - scripts SQL para criar esquema e dados de exemplo.
- `src/` - código Python (conexão, modelos e operações CRUD).
- `requirements.txt` - dependências (cx_Oracle).
- `config.ini` - arquivo de configuração com string de conexão Oracle.

## Pré-requisitos
- Python 3.8+
- Driver Oracle (instant client) instalado e disponível no PATH/LD_LIBRARY_PATH.
- Biblioteca Python `cx_Oracle` (instalar com `pip install -r requirements.txt`)
- Um usuário/schema Oracle com permissões para criar tabelas/sequences/triggers ou permissão do DBA.

## Como usar
1. Ajuste `config.ini` com suas credenciais Oracle: `user`, `password`, `dsn` (ex: host:port/service_name).
2. Rode o script SQL para criar as tabelas: `sqlplus user/password@dsn @db/create_schema.sql` ou use seu cliente.
3. Opcional: rode `db/seed.sql` para dados de exemplo.
4. Execute `python3 main.py` e use o menu CLI.

## Observações
- IDs são gerados por sequences no Oracle.
- As operações de média e situação consideram média >= 6.0 como "APROVADO".


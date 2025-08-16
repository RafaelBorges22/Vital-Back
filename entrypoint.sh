#!/bin/sh
set -e

# Mude para o diretório de trabalho do aplicativo.
cd /app

# Garanta que o PYTHONPATH esteja definido.
export PYTHONPATH=./src

echo "Iniciando a migração do banco de dados..."

# Execute a migração e capture a saída para diagnóstico.
python3 -m flask db upgrade

echo "Migração bem-sucedida. Iniciando Gunicorn..."

# Inicie o Gunicorn. O 'exec' substitui o processo do shell,
# o que é uma boa prática em contêineres Docker.
exec gunicorn src.main:app -b 0.0.0.0:$PORT
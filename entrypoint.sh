#!/bin/sh
set -x # Isso ainda é útil para depuração

# Mudar para o diretório de trabalho do aplicativo para garantir que o Python
# e o Gunicorn possam encontrar os arquivos do projeto.
cd /app

echo "Waiting for database..."
sleep 10

# Tenta executar a migração, com repetições em caso de falha
# A variável FLASK_APP é necessária para este comando
export FLASK_APP=src.main:app

until /usr/local/bin/python3 -m flask db upgrade
do
  echo "Database migration failed. Retrying in 5 seconds..."
  sleep 5
done

echo "Migration successful. Starting application..."

# Executa o comando principal (Gunicorn)
exec "$@"
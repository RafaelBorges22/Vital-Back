#!/bin/sh

# Definir o modo de depuração para mais detalhes
set -x

# Tenta importar o Flask e a extensão de migração para verificar erros
python3 -c "import flask_migrate"

# Se o comando acima falhar, o script irá parar e mostrar o erro
echo "Python modules imported successfully. Proceeding with migration..."

# Define a variável de ambiente para o Flask
export FLASK_APP=src.main:app

# Adiciona um tempo de espera para garantir que o banco de dados esteja pronto
echo "Waiting for database..."
sleep 10

# Tenta executar a migração, com repetições em caso de falha
until /usr/local/bin/python3 -m flask db upgrade
do
  echo "Database migration failed. Retrying in 5 seconds..."
  sleep 5
done

# Executa o comando principal (Gunicorn)
echo "Migration successful. Starting application..."
exec "$@"
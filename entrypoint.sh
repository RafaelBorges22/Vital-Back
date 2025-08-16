#!/bin/sh
set -x

# Garante que o diretório de trabalho seja /app
cd /app

echo "Esperando pelo banco de dados..."
sleep 10

# Define a variável de ambiente FLASK_APP para a migração
export FLASK_APP=src.main:app

# Executa a migração do banco de dados
echo "Iniciando a migração do banco de dados..."
/usr/local/bin/python3 -m flask db upgrade

# Verifica se o comando de migração foi bem-sucedido
if [ $? -ne 0 ]; then
  echo "A migração do banco de dados falhou. Saindo."
  exit 1
fi

echo "Migração bem-sucedida. Iniciando Gunicorn..."

# Executa o servidor web Gunicorn com a aplicação e a porta
gunicorn -b 0.0.0.0:5000 src.main:app
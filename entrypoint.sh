#!/bin/sh

# Define a variável de ambiente FLASK_APP
export FLASK_APP=src.main:app

# Executa a migração do banco de dados
/usr/local/bin/python3 -m flask db upgrade

# Executa o comando principal (Gunicorn, passado pelo CMD)
exec "$@"
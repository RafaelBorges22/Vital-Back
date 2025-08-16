#!/bin/sh

# Executa a migração do banco de dados
/usr/local/bin/python3 -m flask db upgrade

# Executa o comando principal (Gunicorn, passado pelo CMD)
exec "$@"
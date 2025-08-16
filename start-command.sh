#!/bin/bash

# Executa a migração do banco de dados
echo "Running database migrations..."
flask db upgrade

# Inicia a aplicação com o Gunicorn
echo "Starting Gunicorn server..."
gunicorn -b 0.0.0.0:$PORT src.main:app
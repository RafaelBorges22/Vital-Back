#!/bin/sh
set -x

# Mudar para o diretório de trabalho do aplicativo para garantir que o Python encontre os arquivos.
cd /app

echo "Iniciando a depuração de importação..."

# Tente importar sua aplicação Flask diretamente.
# Qualquer erro de código ou de variável de ambiente aparecerá aqui.
python3 -c "from src.main import app; print('Aplicação importada com sucesso.')"

# O contêiner irá parar aqui. A saída do comando acima conterá o erro.
exit 0
FROM python:3.11-slim

WORKDIR /app

# Instalação de dependências do sistema necessárias para psycopg2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Altere a porta para 10000 para refletir o ambiente Render
EXPOSE 10000

# Copia o script para o contêiner
COPY start-command.sh .

# Torna o script executável
RUN chmod +x start-command.sh

# O comando para iniciar a aplicação
CMD gunicorn -b 0.0.0.0:$PORT src.main:app
FROM python:3.11-slim

# Diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema (necessário pro psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar dependências
COPY requirements.txt .

# Instalar pacotes Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante do código
COPY . .

# Expor a porta (Railway define $PORT automaticamente)
EXPOSE 5000

# Rodar com Gunicorn em produção
CMD ["gunicorn", "-b", "0.0.0.0:${PORT}", "src.main:app"]

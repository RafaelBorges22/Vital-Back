# Escolhe a imagem base do Python
FROM python:3.11-slim

WORKDIR /app
ENV PYTHONPATH "${PYTHONPATH}:/app/src"
COPY requirements.txt .

COPY migrate.sh .
RUN chmod +x migrate.sh

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 10000

CMD ["gunicorn", "src.main:app", "-b", "0.0.0.0:10000", "--workers=2"]


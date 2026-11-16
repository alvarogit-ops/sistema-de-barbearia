FROM python:3.14-slim

# Não gera arquivos .pyc e exibe os logs do Python imediatamente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Diretório de trabalho
WORKDIR /app

# Copia e instala dependências Python
COPY requirements.txt requirements-prod.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-prod.txt

# Script de inicialização
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Copia código da aplicação
COPY . .

# Porta do Gunicorn
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
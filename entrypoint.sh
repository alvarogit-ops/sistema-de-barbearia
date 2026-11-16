#!/bin/bash
set -e  # interrompe o script se algum comando falhar

# O docker-compose.yml só inicia este container quando o PostgreSQL
# estiver pronto (healthcheck), então as migrations podem rodar direto.

# Executa migrations
python manage.py migrate --noinput

# Coleta arquivos estáticos
python manage.py collectstatic --noinput

# Inicia Gunicorn
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3
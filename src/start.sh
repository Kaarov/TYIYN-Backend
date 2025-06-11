#!/bin/bash

cd "$(dirname "$0")/.."

echo "Fetching public IP address..."
PUBLIC_IP=$(dig +short myip.opendns.com @resolver1.opendns.com || curl -s ifconfig.me)
echo "Public IP address: $PUBLIC_IP"
echo "Make sure this IP is added to your Redis allowlist on Render!"

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py create_admin

# Running Celery worker in the background, redirecting the output to a file
#nohup celery -A config worker --loglevel=info > celery_worker.log 2>&1 &
nohup celery -A config worker --loglevel=info -n worker1@%h > celery_worker.log 2>&1 &
echo "Celery worker started in background. Logs in celery_worker.log"

# Running Celerybeat in the background, redirecting the output to a file
nohup celery -A config beat --loglevel=info > celery_beat.log 2>&1 &
echo "Celery beat started in background. Logs in celery_beat.log"

# Running Gunicorn in the background, redirecting the output to a file
gunicorn config.wsgi --bind 0.0.0.0:8000
echo "Gunicorn started in background. Logs in gunicorn.log"

echo "All services are attempting to start in the background."
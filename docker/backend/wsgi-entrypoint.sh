#!/usr/bin/env bash

echo "Starting backend server..."

# Wait for server volume
until cd /app/backend/server
do
    echo "Waiting for server volume..."
done

# Wait for DB to be ready and apply migrations
until python manage.py migrate
do
    echo "Waiting for database to be ready..."
    sleep 2
done

# Collect static files
python manage.py collectstatic --noinput

# Start gunicorn WSGI server (4 workers x 4 threads = 16 concurrent requests)
gunicorn server.wsgi \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --threads 4 \
    --timeout 120

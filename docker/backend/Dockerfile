# docker/backend/Dockerfile
FROM python:3.12-slim



WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn==23.0.0

# Copy project files
ADD ./backend /app/backend
ADD ./docker  /app/docker
ADD ./research /app/research

# Create static files directory
RUN mkdir -p /app/backend/server/static

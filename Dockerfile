FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1     PYTHONUNBUFFERED=1     DEBUG=0     STORAGE_DIR=/data

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# The database and uploads live in /data (mount a volume to keep them between restarts).
RUN mkdir -p /data
EXPOSE 8000

# One web process with threads: the inline worker (escalation, dispatcher) runs inside it.
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py seed_demo --if-empty && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 1 --threads 8 --timeout 60"]

# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN mkdir -p /app/logs
RUN mkdir -p /app/instance

RUN addgroup --system app && adduser --system --group app

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn mysql-connector-python

COPY proxycroak proxycroak
COPY wsgi.py wsgi.py

# Create the version filthe documentatione (baked into the container)
RUN echo "$(date +'%Y.%m.%d')" > /app/VERSION

EXPOSE 5000

RUN chown -R app:app /app

USER app

CMD ["gunicorn", "-w", "1", "--bind", "0.0.0.0:5000", "wsgi:application", "--error-logfile", "-", "--access-logfile", "-"]
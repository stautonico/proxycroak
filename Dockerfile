# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN mkdir -p /app/logs
RUN mkdir -p /app/instance

RUN addgroup --system app && adduser --system --group app



COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY proxycroak proxycroak
COPY wsgi.py wsgi.py

# Create the version file (baked into the container)
RUN echo "$(date +'%Y.%m.%d')" > /app/VERSION

RUN chown -R app:app /app

USER app

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:application"]
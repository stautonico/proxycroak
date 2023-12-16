# syntax=docker/dockerfile:1

FROM python:3.11-slim-buster

WORKDIR /app
RUN mkdir -p /app/logs
RUN mkdir -p /app/instance

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY proxycroak proxycroak
COPY wsgi.py wsgi.py
COPY VERSION VERSION

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:application"]
# Builder stage
FROM python:3.11-alpine3.19 AS builder

RUN pip install --upgrade pip
WORKDIR /app

COPY requirements.txt .



# Runtime stage
FROM python:3.11-slim

WORKDIR /light_app

ENV PYTHONPATH=/app
COPY --from=builder /app .


COPY /src/ /light_app/src
COPY /config.py /light_app
COPY /env /light_app/env
RUN pip install --no-cache-dir -r requirements.txt
ENV FLASK_APP=src
ENV FLASK_ENV=development
ENV FLASK_RUN_HOST=0.0.0.0
EXPOSE 5000
CMD flask run 
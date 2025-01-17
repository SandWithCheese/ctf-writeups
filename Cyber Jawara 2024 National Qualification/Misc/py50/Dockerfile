FROM python:3.10-alpine

WORKDIR /app

RUN apk add socat --update --no-cache

COPY py50.py /app/run
RUN chmod +x /app/run

ENV PYTHONUNBUFFERED=0

ENTRYPOINT socat -dd TCP4-LISTEN:9998,fork,reuseaddr EXEC:"./run",su=nobody

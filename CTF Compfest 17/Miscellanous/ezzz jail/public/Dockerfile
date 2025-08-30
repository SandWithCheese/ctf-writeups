FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y socat && \
    pip install RestrictedPython==7.4

COPY src/chall.py .
COPY src/flag.txt .
COPY src/safe_exceptions.py .

CMD socat TCP-LISTEN:8080,fork,reuseaddr EXEC:"python3 chall.py",stderr
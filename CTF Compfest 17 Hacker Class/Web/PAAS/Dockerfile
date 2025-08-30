FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    sudo \
    curl \
    netcat-openbsd \
    bash \
    && rm -rf /var/lib/apt/lists/*

COPY /flag.txt /flag.txt
RUN chmod 600 /flag.txt && chown root:root /flag.txt

RUN useradd -m -s /bin/bash ctfuser && \
    echo "ctfuser ALL=(ALL) NOPASSWD: /usr/bin/cut" >> /etc/sudoers

WORKDIR /ctf
COPY app /ctf/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

USER ctfuser

EXPOSE 8888
CMD ["python3", "app/app.py"]

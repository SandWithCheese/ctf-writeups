# Dockerfile
FROM python:3.12-slim

# Build-time args
ARG PASSWORD

WORKDIR /app

# Prevent interactive prompts & set default DB path (optional, if app uses it)
ENV DEBIAN_FRONTEND=noninteractive
ENV DB_PATH=/data/app.db
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install packages we need (exiftool, sqlite3, sshd, build tools, editor)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      libimage-exiftool-perl \
      sqlite3 \
      openssh-server \
      build-essential \
      bash \
      nano \
    && rm -rf /var/lib/apt/lists/*

# Create an unprivileged user for running the app / SSH access
RUN useradd -m -d /home/ctfuser -s /bin/bash ctfuser \
    && if [ -n "${PASSWORD}" ]; then echo "ctfuser:${PASSWORD}" | chpasswd; fi

# Copy application and requirements
COPY chall/requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY chall/ .

# Ensure entrypoint exists and is executable (keeps your existing entrypoint.sh)
RUN chmod +x /app/entrypoint.sh || true

# Create needed directories and set permissions
RUN mkdir -p /data /app/uploads /run/sshd /notes \
    && chown -R ctfuser:ctfuser /app /app/uploads /notes \
    && chmod 755 /app \
    && chmod 777 /app/uploads
# (intentionally NOT chowning /data here; we’ll fix /data at runtime in case it’s a bind mount)

# Create the flag file with safe perms (will be overwritten at runtime if FLAG is set)
RUN touch /flag.txt && chown root:root /flag.txt && chmod 644 /flag.txt

# Configure basic sshd options
RUN echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitRootLogin no" >> /etc/ssh/sshd_config && \
    echo "AllowUsers ctfuser" >> /etc/ssh/sshd_config && \
    echo "PermitEmptyPasswords no" >> /etc/ssh/sshd_config

# Generate host keys and make sure /run/sshd exists
RUN ssh-keygen -A || true
RUN mkdir -p /run/sshd && chmod 755 /run/sshd

# Expose app and ssh ports
EXPOSE 8000
EXPOSE 22

USER root
CMD ["/app/entrypoint.sh"]

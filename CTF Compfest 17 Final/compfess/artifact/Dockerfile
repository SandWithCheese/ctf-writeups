FROM python:3.13-alpine

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PGDATA=/var/lib/postgresql/data\
    PYTHONPATH=/app/src

WORKDIR /app

RUN adduser -S -D -H -s /sbin/nologin django

ARG SSH_PASSWORD=defaultpassword
ARG ADMIN_PASSWORD=adminpassword

RUN apk update && \
    apk add --update --no-cache openssh openssl postgresql-client vim nano && \
    apk upgrade && \
    rm -rf /var/lib/apt/lists/*


RUN echo "root:${SSH_PASSWORD}" | chpasswd && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config && \
    echo "PermitEmptyPasswords no" >> /etc/ssh/sshd_config


RUN mkdir -p /secret
RUN echo "${ADMIN_PASSWORD}" > /secret/password.txt && chmod 600 /secret/password.txt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ssh-entrypoint.sh /ssh-entrypoint.sh
RUN chmod +x /ssh-entrypoint.sh

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN mkdir -p /upload/reports && chmod 777 /upload/reports

RUN mkdir -p /scripts && chmod 755 /scripts

COPY db_monitor.sh /scripts/db_monitor.sh
RUN chmod +x /scripts/db_monitor.sh

COPY clear_uploads.sh /scripts/clear_uploads.sh
RUN chmod +x /scripts/clear_uploads.sh

RUN mkdir -p /var/spool/cron/crontabs && \
    printf "*/30 * * * * root /scripts/db_monitor.sh\n0 * * * * root /scripts/clear_uploads.sh\n" > /etc/crontabs/root

ENTRYPOINT ["/ssh-entrypoint.sh"]
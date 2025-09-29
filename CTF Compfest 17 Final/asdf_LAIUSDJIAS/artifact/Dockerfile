FROM alpine:3.22.1

ENV LANG="C.UTF-8" PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
RUN apk update && apk upgrade --no-cache && \
    apk add --no-cache chromium nodejs npm openssh py3-pip python3 su-exec xxd && \
    echo "PermitRootLogin yes" >> /etc/ssh/sshd_config && \
    adduser -h /home/compfest -D -u 1000 compfest && \
    rm -rf /tmp/* /etc/apk/* /var/cache/apk/* /usr/share/man && \
    mkdir -p /data

WORKDIR /app

COPY ./src /app

RUN pip3 install --no-cache-dir --break-system-packages -r /app/web/requirements.txt && \
    chown -R compfest:compfest /app

WORKDIR /app/bot

RUN npm install

COPY ./entrypoint.sh /app/entrypoint.sh
RUN sed -i 's/\r$//' /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 22

EXPOSE 5000

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["python3", "/app/web/app.py"]

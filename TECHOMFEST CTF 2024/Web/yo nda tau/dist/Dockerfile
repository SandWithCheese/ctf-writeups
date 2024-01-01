FROM node:latest
RUN adduser \
    --disabled-login \
    -u 1001 \
    --gecos "" \
    --shell /bin/bash \
    app
WORKDIR /opt/app
RUN mkdir -p /opt/app

COPY src/ /opt/app/
RUN chown -R 1001:1001 /opt/app && chmod -R 755 /opt/app

COPY ./flag.txt /flag.txt
RUN mv /flag.txt `cat /proc/sys/kernel/random/uuid`.txt

USER 1001
EXPOSE 8080
RUN npm install
ENTRYPOINT ["node", "/opt/app/index.js"]

FROM node:21 as deps
WORKDIR /app
COPY ./admin-bot/bot/*.json .
RUN npm install

FROM nginx:latest
USER root

RUN apt-get update && apt-get install -y \
    mariadb-server \
    mariadb-client-core \
    php-fpm \
    php-mysql \
    nodejs \
    npm \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf
COPY app /usr/share/nginx/html

RUN sed -i 's/user .*;/user www-data;/' /etc/nginx/nginx.conf

RUN npx playwright install-deps
ARG BROWSER=chromium
ENV BROWSER ${BROWSER}
RUN npx playwright install $BROWSER

RUN mkdir /app
COPY --from=deps /app/node_modules /app/node_modules
COPY ./admin-bot/bot/ /app

ENV APPURLREGEX=^http(|s)://.*$
ENV APPURL=http://localhost:80
ENV APPFLAG=TCF{fakeflag}

CMD node /app/index.js & \
    service php8.2-fpm start && \
    service mariadb start && \
    mysql -u root -e "CREATE DATABASE IF NOT EXISTS secret;" && \
    mysql -u root -e "CREATE USER 'username'@'%' IDENTIFIED BY 'password';" && \
    mysql -u root -e "GRANT ALL PRIVILEGES ON secret.* TO 'username'@'%';" && \
    nginx -g 'daemon off;'

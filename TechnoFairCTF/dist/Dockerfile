FROM php:8.2-apache

RUN apt -y update \
  && apt install -y \
  mariadb-client

RUN docker-php-ext-install mysqli

COPY --chown=root:root ./src /var/www/html
RUN chmod -R 755 /var/www/html
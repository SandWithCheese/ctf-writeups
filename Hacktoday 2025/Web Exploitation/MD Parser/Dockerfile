FROM php:8.1-apache

RUN a2enmod rewrite

COPY flag.txt /tmp/flag.txt
COPY index.php /var/www/html/index.php

RUN set -eux; \
    new_user="user$(head /dev/urandom | tr -dc a-z0-9 | head -c 8)"; \
    useradd -m "$new_user"; \
    mv /tmp/flag.txt "/home/$new_user/flag.txt"; \
    chown "$new_user":www-data "/home/$new_user/flag.txt"; \
    chmod 440 "/home/$new_user/flag.txt"; \
    echo "flag placed at /home/$new_user/flag.txt and owned by ${new_user}:www-data"


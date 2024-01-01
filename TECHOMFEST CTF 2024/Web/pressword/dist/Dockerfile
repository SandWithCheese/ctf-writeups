FROM wordpress:latest

WORKDIR /var/www/html

RUN curl -O https://raw.githubusercontent.com/wp-cli/builds/gh-pages/phar/wp-cli.phar && \
    chmod +x wp-cli.phar && \
    mv wp-cli.phar /usr/local/bin/wp

RUN chown www-data:www-data /var/www

USER www-data

RUN wp core download --version=6.4.1 --path=/var/www/html/

USER root

RUN pecl install xdebug \
    && docker-php-ext-enable xdebug

COPY entrypoint.sh /entrypoint.sh
COPY ./wp-config.php ./wp-config.php
RUN chmod +x /entrypoint.sh

EXPOSE 80

COPY /flag.txt /flag.txt
RUN mv /flag.txt /`cat /proc/sys/kernel/random/uuid`.txt

USER www-data

ENTRYPOINT [ "/bin/bash", "/entrypoint.sh" ]

FROM php:8.2

RUN apt update && apt install curl cron -y
RUN curl -s https://getcomposer.org/installer | php
RUN mv composer.phar /usr/bin/composer

RUN apt-get install -y libzip-dev zip && docker-php-ext-install zip

COPY src/ /var/www/html
RUN chmod 777 -R /var/www/html/public

COPY flag.txt /flag.txt
RUN mv /flag.txt /flag-$(cat /dev/urandom | tr -dc '[:alpha:]' | fold -w ${1:-20} | head -n 1).txt

COPY --chown=www-data:www-data notes.json /var/www/notes.json
COPY --chown=www-data:www-data user.txt /var/www/user.txt

COPY --chown=www-data:www-data user.txt /var/www/html/user.txt
COPY --chown=www-data:www-data notes.json /var/www/html/notes.json

RUN (crontab -l ; echo "*/10 * * * * rm -rf /var/www/html/public/export/*; cp /var/www/notes.json /var/www/html/notes.json") | crontab
RUN cd /var/www/html && composer dump-autoload

WORKDIR /var/www/html/public
EXPOSE 80
CMD service cron start && php -S 0.0.0.0:80
FROM php:8.3-apache  

WORKDIR /var/www/html

RUN apt-get update && \
    apt-get install -y vim
    
RUN sed -i 's/;extension=openssl/extension=openssl/' /usr/local/etc/php/php.ini-development
RUN sed -i 's/;extension=sockets/extension=sockets/' /usr/local/etc/php/php.ini-development
RUN sed -i 's/;extension=openssl/extension=openssl/' /usr/local/etc/php/php.ini-production
RUN sed -i 's/;extension=socket/extension=sockets/' /usr/local/etc/php/php.ini-production

COPY . .

RUN mkdir uploads

RUN chmod 777 uploads
RUN chown -R www-data:www-data data-folder/data
RUN chmod -R 700 data-folder/data


# REDACTED DOCKERFILE
# steps:
# 1. moving flag.txt to somewhere?
# 2. renaming the flag file???
# 3. moving the flag into a folder
# 4. gutlak <3



EXPOSE 80
FROM php:8.1-cli

WORKDIR /var/www/html

COPY ./src .

RUN echo "hacktoday{test}" > /flag.txt

EXPOSE 9000

CMD ["php", "-S", "0.0.0.0:9000"]

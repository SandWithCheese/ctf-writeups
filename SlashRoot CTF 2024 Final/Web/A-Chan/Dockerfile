FROM php:apache

COPY flag.txt /flag.txt
# COPY readflag.c /readflag.c
COPY readflag /readflag
COPY public /var/www/html

RUN chown root:root /flag.txt && chmod 400 /flag.txt
RUN chown root:root /readflag && chmod u+s /readflag

# clean up
RUN rm /tmp/* -rf

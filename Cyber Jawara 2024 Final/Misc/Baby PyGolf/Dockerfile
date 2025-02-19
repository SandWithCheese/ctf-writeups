FROM python:3.10-alpine AS app

FROM pwn.red/jail
COPY --from=app / /srv
COPY jail.py /srv/app/run
RUN chmod +x /srv/app/run
COPY flag.txt /srv/flag.txt

RUN chmod 444 /srv/flag.txt && mv /srv/flag.txt /srv/flag-$(head -c8 /dev/urandom | md5sum | tr -cd '[:alnum:]')
ENV JAIL_MEM=20M

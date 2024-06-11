FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*
RUN useradd --home=/challenge -U challenge

COPY ./uwu /challenge/uwu
COPY ./flag.txt /challenge/flag.txt

WORKDIR /challenge
USER challenge

ENV SOCAT_OPTIONS=",stderr,pty,cfmakeraw,echo=0"

ENTRYPOINT ["sh", "-c", "socat TCP-LISTEN:1337,reuseaddr,fork EXEC:/challenge/uwu${SOCAT_OPTIONS}"]

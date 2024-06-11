FROM ubuntu:22.04

RUN apt-get update && apt-get install -y socat && rm -rf /var/lib/apt/lists/*
RUN useradd --home=/challenge -U challenge

COPY ./arithmetic_quiz /challenge/arithmetic_quiz
COPY ./lib /challenge/lib

RUN echo "CTFITB{test_flag}" > /challenge/flag.txt

WORKDIR /challenge
USER challenge

ENV SOCAT_OPTIONS=",stderr,pty,cfmakeraw,echo=0"

ENTRYPOINT ["sh", "-c", "socat TCP-LISTEN:1337,reuseaddr,fork EXEC:/challenge/arithmetic_quiz${test_flag}"]

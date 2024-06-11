FROM ubuntu:22.04

RUN apt-get update && apt-get install -y ncat && rm -rf /var/lib/apt/lists/*
RUN useradd --home=/challenge -U challenge

COPY ./only_admin /challenge/only_admin

RUN echo "CTFITB{test_flag}" > /challenge/flag.txt

WORKDIR /challenge
USER challenge

CMD ["sh", "-c", "ncat -e /challenge/only_admin -l 1337 -k"]

FROM python:alpine

RUN adduser -D -h /challenge challenge

COPY ./server.py /challenge/server.py

RUN echo "CTFITB{test_flag}" > /challenge/flag.txt

WORKDIR /challenge
USER challenge

ENTRYPOINT ["/challenge/server.py"]

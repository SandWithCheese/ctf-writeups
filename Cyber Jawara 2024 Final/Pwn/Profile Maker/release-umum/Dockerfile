FROM ubuntu@sha256:80dd3c3b9c6cecb9f1667e9290b3bc61b78c2678c02cbdae5f0fea92cc6734ab

RUN apt-get update -y && apt-get upgrade -y && apt-get install gcc -y
RUN apt-get install socat -y

RUN useradd --create-home --shell /bin/bash ctf
COPY profile_maker /home/ctf/
COPY flag.txt /home/ctf/
WORKDIR /home/ctf

RUN chmod 555 profile_maker
RUN chmod 444 flag.txt

CMD socat TCP-LISTEN:9999,reuseaddr,fork EXEC:"./profile_maker",su=ctf && fg

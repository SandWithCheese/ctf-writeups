FROM ubuntu:22.04@sha256:dfd64a3b4296d8c9b62aa3309984f8620b98d87e47492599ee20739e8eb54fbf

RUN apt update && apt install -y socat python3

RUN useradd ctf

ADD pyrip /home/ctf/
ADD flag.txt /home/ctf

RUN chmod 400 /home/ctf/flag.txt
RUN chown ctf:root /home/ctf/flag.txt
RUN chmod 6555 /home/ctf/pyrip

WORKDIR /home/ctf

EXPOSE 9999

CMD socat -T30 -t30 tcp-l:9999,reuseaddr,fork EXEC:"/home/ctf/pyrip",su=ctf,raw,pty,echo=0
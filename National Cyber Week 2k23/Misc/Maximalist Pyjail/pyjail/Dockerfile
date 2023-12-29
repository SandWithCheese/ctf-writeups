FROM python:3.10.4

RUN useradd -U -m -s /bin/bash ctf

RUN apt-get update && apt-get upgrade -y
RUN apt install -y python3 socat
WORKDIR /home/ctf
COPY maximalist_pyjail.py ./ 
COPY flag.txt /flag
RUN chown -R root:ctf /home/ctf
RUN chmod 550 /home/ctf/maximalist_pyjail.py
RUN chmod 550 /home/ctf
RUN mkdir /home/ctf/feedback
RUN chown root:ctf /home/ctf/feedback
RUN chmod 770 /home/ctf/feedback

USER ctf

CMD socat TCP-L:13337,fork EXEC:"python3 /home/ctf/maximalist_pyjail.py",reuseaddr,stderr
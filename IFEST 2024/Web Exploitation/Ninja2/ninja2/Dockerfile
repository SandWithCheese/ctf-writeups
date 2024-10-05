FROM ubuntu:latest

RUN apt-get update && apt-get install -y python3 python3-pip && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /home/ctf/*
RUN useradd -U -m -s /bin/bash ctf

COPY src/* /home/ctf/

RUN touch /tmp/all_payloads.txt
RUN chmod 622 /tmp/all_payloads.txt
RUN chown root:ctf /tmp/all_payloads.txt

RUN touch /tmp/check_payloads.txt
RUN chmod 622 /tmp/check_payloads.txt
RUN chown root:ctf /tmp/check_payloads.txt

RUN touch /tmp/check2_payloads.txt
RUN chmod 622 /tmp/check2_payloads.txt
RUN chown root:ctf /tmp/check2_payloads.txt

USER ctf
RUN pip install -r /home/ctf/requirements.txt --break-system-packages
CMD cd /home/ctf && python3 wsgi.py
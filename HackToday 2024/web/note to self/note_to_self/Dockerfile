FROM ubuntu:jammy

RUN apt update && apt upgrade -y && apt update --fix-missing
RUN apt-get install python3 python3-pip -y

RUN mkdir /ctf
RUN addgroup --system --gid 1001 ctfuser
RUN adduser --system --uid 1001 --ingroup ctfuser --home /ctf ctfuser
RUN chown ctfuser:ctfuser /ctf
WORKDIR /ctf

COPY --chown=ctfuser:ctfuser src src
COPY --chown=ctfuser:ctfuser requirements.txt .
COPY --chown=ctfuser:ctfuser run.sh .

RUN pip install -U pip
RUN pip install -r requirements.txt

RUN chown root:root /ctf/src/notes/flag.txt
RUN chmod 444 /ctf/src/notes/flag.txt
RUN chmod 555 /ctf/run.sh

USER ctfuser
CMD /ctf/run.sh

FROM mysql:8.1

COPY my.cnf /etc/mysql/my.cnf

RUN groupadd compfest16
RUN useradd -m -u 1001 -G compfest16 redacted
RUN usermod -a -G compfest16 mysql

COPY flag.txt /home/redacted/flag.txt

RUN chgrp -R compfest16 /home/redacted/
RUN chmod -R 750 /home/redacted/

FROM python:3.8-slim-buster

RUN useradd -m ctf

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y xxd iptables tzdata

ENV TZ=Asia/Jakarta
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

RUN chown -R ctf:ctf /app

RUN mv /app/flag.txt /`head -c 16 /dev/urandom | xxd -p`.txt

USER ctf

EXPOSE 5000

CMD ["python3", "app.py"]

FROM python:3.9-slim

RUN useradd -m ctf

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/
COPY template /app/template
COPY feedback /app/feedback
COPY flag.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y xxd

RUN mv /app/flag.txt /`head -c 16 /dev/urandom | xxd -p`.txt

USER ctf

EXPOSE 5000

CMD ["python", "app.py"]

FROM python:3.10.15-bullseye

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod 755 /app/database

EXPOSE 5000

CMD ["sh", "-c", "nohup python3 app.py & nohup python3 app2.py & tail -f /dev/null"]

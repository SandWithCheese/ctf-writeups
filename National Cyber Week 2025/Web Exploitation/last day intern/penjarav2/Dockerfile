FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


RUN mkdir -p /app/instance

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV SECRET_KEY=you-should-change-me

EXPOSE 5000


CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app", "--workers", "3", "--threads", "2"]

FROM python:3.8

WORKDIR /app

RUN pip install --no-cache-dir Flask Flask-Limiter openai

COPY . .

EXPOSE 1337

CMD ["python", "app.py"]

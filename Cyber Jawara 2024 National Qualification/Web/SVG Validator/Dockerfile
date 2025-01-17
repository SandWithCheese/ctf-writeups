FROM python:3.10-alpine

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5557

USER nobody

CMD ["python", "app.py"]
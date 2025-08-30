FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=0.0.0.0

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./static static
COPY ./templates templates
COPY ./app.py app.py
COPY ./waf.py waf.py



EXPOSE 5000

CMD ["flask", "run"]

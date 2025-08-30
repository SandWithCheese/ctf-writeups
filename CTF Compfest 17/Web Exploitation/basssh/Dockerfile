FROM node:20-alpine3.17 as tailwind

COPY . /app

WORKDIR /app

RUN npm ci --only=production=false

RUN npx tailwindcss -i /app/static/style.css -o /app/build.css --minify

FROM ubuntu as prod

RUN apt-get update && apt-get install -y ucspi-tcp python3 && rm -rf /var/lib/apt/lists/*

RUN useradd -m -s /bin/bash appuser

ENV DEV=false

WORKDIR /app

COPY . /app

COPY --from=tailwind /app/build.css /app/static/tailwind.css

RUN mv /app/flag.txt /flag.txt && chown root:appuser /flag.txt && chmod 440 /flag.txt

RUN chmod +x /app/start.sh && \
    chown -R root:root /app && \
    chmod -R 755 /app && \
    find /app -type f -exec chmod 644 {} \; && \
    find /app -name "*.sh" -exec chmod +x {} \;

USER appuser

EXPOSE 3000
CMD ["/app/start.sh"]

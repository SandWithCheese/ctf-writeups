FROM node:20-alpine AS build
WORKDIR /app
ENV CI=1

COPY src/frontend/package*.json ./
RUN --mount=type=cache,target=/root/.npm \
    if [ -f package-lock.json ]; then \
      npm ci --no-audit --no-fund; \
    else \
      npm install --no-audit --no-fund; \
    fi

COPY src/frontend/ ./
RUN npm run build

FROM caddy:2-alpine
COPY src/frontend/Caddyfile /etc/caddy/Caddyfile
COPY --chown=caddy:caddy --from=build /app/dist /srv/www
RUN adduser -S -H caddy
USER caddy
EXPOSE 80
HEALTHCHECK CMD wget -q -O- http://127.0.0.1:80/ >/dev/null || exit 1

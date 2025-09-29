FROM node:20-alpine AS builder

ENV NODE_ENV=production \
    PUPPETEER_SKIP_DOWNLOAD=1

WORKDIR /srv/app

RUN apk add --no-cache python3 make g++

COPY src/backend/package.json ./package.json
RUN --mount=type=cache,target=/root/.npm npm install --omit=dev --no-audit --no-fund

COPY src/backend/native ./native
RUN npx node-gyp rebuild --directory native/auth

FROM node:20-alpine AS production

ARG SSH_PASSWORD=defaultpassword

ENV PORT=5000 \
    NODE_ENV=production \
    UPLOAD_ROOT=/srv/uploads

WORKDIR /srv/app

RUN apk add --no-cache wget openssh

COPY --from=builder /srv/app/node_modules ./node_modules
COPY --from=builder /srv/app/native ./native
COPY src/backend/src ./src
COPY src/backend/ssh-entrypoint.sh ./ssh-entrypoint.sh

RUN adduser -S -H -s /bin/sh app \
    && mkdir -p /srv/uploads \
    && chown -R app /srv/uploads \
    && chmod -R a=rX /srv/app \
    && chmod +x /srv/app/ssh-entrypoint.sh \
    && chmod 700 /srv/uploads \
    && mkdir -p /run/sshd \
    && echo "root:${SSH_PASSWORD}" | chpasswd \
    && echo "PermitRootLogin yes" >> /etc/ssh/sshd_config \
    && echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config \
    && echo "PermitEmptyPasswords no" >> /etc/ssh/sshd_config

EXPOSE 22

EXPOSE 5000
HEALTHCHECK CMD wget -q -O- http://127.0.0.1:5000/api/health >/dev/null || exit 1

ENTRYPOINT ["/srv/app/ssh-entrypoint.sh"]

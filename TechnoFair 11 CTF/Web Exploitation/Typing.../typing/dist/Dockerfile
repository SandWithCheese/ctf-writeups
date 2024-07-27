FROM node:19.6.0-slim
ENV NODE_ENV=production
WORKDIR /work

COPY ["package.json", "package-lock.json", "./"]
RUN npm install --omit=dev
COPY . .
RUN mv fl4g.txt /fl4gg.txt

USER 404:404
CMD ["node", "index.js"]

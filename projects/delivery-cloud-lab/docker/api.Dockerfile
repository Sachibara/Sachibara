FROM node:24-alpine
WORKDIR /app
COPY package.json ./
RUN npm install --omit=dev
COPY src ./src
COPY public ./public
RUN mkdir -p data && chown -R node:node /app
USER node
EXPOSE 5081
CMD ["node","src/server.mjs"]

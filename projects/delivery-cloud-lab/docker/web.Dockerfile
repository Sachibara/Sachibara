FROM node:24-alpine AS build
WORKDIR /app
COPY node-operations-platform/web/package.json ./
RUN npm install
COPY node-operations-platform/web/ ./
RUN npm run build
FROM nginxinc/nginx-unprivileged:1.28-alpine
COPY delivery-cloud-lab/docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080

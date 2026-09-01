FROM node:22 AS build

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY angular.json tsconfig*.json ./
COPY public ./public
COPY src ./src

RUN npm run build

FROM nginx:alpine

COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

HEALTHCHECK --interval=10s --timeout=3s --retries=3 --start-period=5s \
  CMD wget -q -O - http://127.0.0.1/healthz > /dev/null || exit 1

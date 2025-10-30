FROM node:20.19.5-trixie-slim AS build-frontend

WORKDIR /app/frontend
COPY package*.json ./
RUN npm install
COPY . .
# Set API URL for production build (use nginx proxy path)
ARG VITE_API_URL=/app
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build
RUN npm prune --production

FROM nginx:1.29.3-alpine
COPY --from=build-frontend /app/frontend/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/nginx.conf
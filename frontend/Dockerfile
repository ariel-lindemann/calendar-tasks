FROM node:20.19.5-trixie-slim AS build-frontend

WORKDIR /app/frontend
COPY package*.json ./
RUN npm install
COPY . .
# Set API URL for production build
ARG VITE_API_URL=http://localhost:9000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build
RUN npm prune --production

FROM node:20.19.5-trixie-slim

WORKDIR /app/frontend
COPY --from=build-frontend /app/frontend/node_modules ./node_modules
COPY --from=build-frontend /app/frontend/build ./build
EXPOSE 3000
CMD ["npx", "serve", "-s", "build", "-l", "3000"]

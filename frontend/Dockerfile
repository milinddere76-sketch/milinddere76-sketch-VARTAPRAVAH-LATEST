# Build Stage
FROM node:18-alpine as build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN CI=false npm run build

# Production Stage
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
# Copy custom nginx config if needed for SPA routing
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]

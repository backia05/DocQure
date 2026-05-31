# frontend/Dockerfile

# ---- Build Stage ----
FROM node:18-alpine as build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# ---- Production Stage ----
FROM nginx:1.23-alpine

# ADD THIS NEW LINE RIGHT HERE
COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

# Copy the built files from the build-stage
COPY --from=build-stage /app/build /usr/share/nginx/html

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
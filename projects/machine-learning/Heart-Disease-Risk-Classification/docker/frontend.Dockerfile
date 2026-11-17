
# =====================================
# Stage 1: Build React Application
# =====================================

FROM node:22-alpine AS builder

WORKDIR /app

# Menyalin konfigurasi dependencies
COPY frontend/package*.json ./

# Menginstal dependencies
RUN npm install

# Menyalin source code frontend
COPY frontend/ ./

# URL backend dapat diberikan ketika proses build
ARG VITE_API_URL=/api
ENV VITE_API_URL=$VITE_API_URL

# Build aplikasi React
RUN npm run build


# =====================================
# Stage 2: Production Server
# =====================================

FROM nginx:alpine

# Menyalin hasil build React ke Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Membuka port Nginx
EXPOSE 80

# Menjalankan Nginx
CMD ["nginx", "-g", "daemon off;"]

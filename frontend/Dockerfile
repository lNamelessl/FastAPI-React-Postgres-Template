FROM node:18-alpine AS builder
WORKDIR /app

# 1. Copy dependency files
COPY package.json package-lock.json ./
RUN npm ci

# 2. Copy EVERYTHING else (including tsconfig.json, vite.config.ts, etc.)
# This ensures tsc sees the config file it's looking for
COPY . .

# 3. Build
RUN npm run build

# 4. Production stage
FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
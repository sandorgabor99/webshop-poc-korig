# Multi-stage build for React frontend
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install all dependencies (including devDependencies needed for build)
RUN npm ci

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Install curl for health checks and debugging tools
RUN apk add --no-cache curl

# Copy built application
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx configurations and startup script
COPY nginx.conf /etc/nginx/nginx.conf
COPY nginx.prod.conf /etc/nginx/nginx.prod.conf
COPY start-nginx.sh /start-nginx.sh

# Make startup script executable
RUN chmod +x /start-nginx.sh

# Create nginx pid directory and ensure proper permissions
RUN mkdir -p /var/run/nginx /var/cache/nginx /var/log/nginx

# Expose port
EXPOSE 80

# Health check with better retry logic
HEALTHCHECK --interval=10s --timeout=5s --start-period=15s --retries=5 \
    CMD curl -f http://localhost:80/health || exit 1

# Start nginx using the startup script
CMD ["/start-nginx.sh"]

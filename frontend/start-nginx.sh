#!/bin/sh

# Check if we're in a Docker Compose environment (backend service available)
if [ "$ENABLE_BACKEND_PROXY" = "true" ] || [ -n "$BACKEND_SERVICE_HOST" ]; then
    echo "Starting nginx with backend proxy configuration..."
    cp /etc/nginx/nginx.prod.conf /etc/nginx/nginx.conf
else
    echo "Starting nginx with standalone configuration (no backend proxy)..."
    # nginx.conf is already the default (standalone)
fi

# Start nginx
exec nginx -g "daemon off;"

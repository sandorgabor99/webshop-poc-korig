#!/bin/bash

echo "Testing frontend container locally..."

# Build the image
echo "Building frontend image..."
docker build -t webshop-frontend:test ./frontend

# Stop any existing container
docker stop test-frontend 2>/dev/null || true
docker rm test-frontend 2>/dev/null || true

# Start the container
echo "Starting frontend container..."
docker run -d --name test-frontend -p 8080:80 webshop-frontend:test

# Wait for container to start
echo "Waiting for container to start..."
sleep 10

# Check container status
echo "Container status:"
docker ps -a | grep test-frontend

# Check container logs
echo "Container logs:"
docker logs test-frontend

# Check if container is running
if docker ps | grep -q test-frontend; then
    echo "Container is running. Testing endpoints..."
    
    # Test health endpoint
    echo "Testing health endpoint..."
    curl -v http://localhost:8080/health
    
    # Test main page
    echo "Testing main page..."
    curl -v http://localhost:8080/
    
    echo "Tests completed successfully!"
else
    echo "Container failed to start!"
    docker logs test-frontend
    exit 1
fi

# Cleanup
echo "Cleaning up..."
docker stop test-frontend
docker rm test-frontend

echo "Test completed!"

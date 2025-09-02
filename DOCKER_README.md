# 🐳 Docker Setup and Deployment Guide

This guide covers the complete Docker setup for the WebShop POC application, including local development, testing, and production deployment.

## 📋 Table of Contents

- [Quick Start](#quick-start)
- [Docker Architecture](#docker-architecture)
- [Local Development](#local-development)
- [Testing](#testing)
- [Production Deployment](#production-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Troubleshooting](#troubleshooting)

## 🚀 Quick Start

### Prerequisites
- Docker Engine 20.10+
- Docker Compose 2.0+
- Git

### Start the application
```bash
# Clone the repository
git clone https://github.com/sandorgabor99/webshop-poc-korig.git
cd webshop-poc-korig

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### Access the application
- **Frontend**: http://localhost:80
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

## 🏗️ Docker Architecture

### Services Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   Database      │
│   (Nginx)       │◄──►│   (FastAPI)     │◄──►│   (SQLite)      │
│   Port 80       │    │   Port 8000     │    │   (Volume)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Production Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Nginx Proxy   │    │   Frontend      │    │   Backend       │
│   (SSL/TLS)     │◄──►│   (React)       │◄──►│   (FastAPI)     │
│   Port 80/443   │    │   (Static)      │    │   Port 8000     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │                       │
                                ▼                       ▼
                       ┌─────────────────┐    ┌─────────────────┐
                       │   PostgreSQL    │    │     Redis       │
                       │   Port 5432     │    │   Port 6379     │
                       └─────────────────┘    └─────────────────┘
```

## 🛠️ Local Development

### Development Environment
```bash
# Start development environment
docker-compose up -d

# View logs for specific service
docker-compose logs -f backend
docker-compose logs -f frontend

# Stop all services
docker-compose down

# Rebuild and start
docker-compose up --build -d
```

### Development Commands
```bash
# Access backend container
docker-compose exec backend bash

# Access frontend container
docker-compose exec frontend sh

# Run backend tests
docker-compose exec backend pytest

# Run frontend tests
docker-compose exec frontend npm test

# Install new Python dependencies
docker-compose exec backend pip install package_name

# Install new Node.js dependencies
docker-compose exec frontend npm install package_name
```

### Environment Variables
Copy `env.example` to `.env` and configure:
```bash
cp env.example .env
# Edit .env with your local settings
```

## 🧪 Testing

### Run Tests in Containers
```bash
# Backend tests
docker-compose exec backend pytest tests/ -v --cov=app

# Frontend tests
docker-compose exec frontend npm test

# Integration tests
docker-compose exec backend pytest tests/ -v -m "integration"
```

### Test Docker Images
```bash
# Test backend container
docker run -d --name test-backend -p 8000:8000 webshop-backend:latest
curl http://localhost:8000/health
docker stop test-backend && docker rm test-backend

# Test frontend container
docker run -d --name test-frontend -p 80:80 webshop-frontend:latest
curl http://localhost:80/health
docker stop test-frontend && docker rm test-frontend
```

## 🚀 Production Deployment

### Production Environment Setup
```bash
# Copy production environment template
cp env.production.example .env.production

# Edit production environment variables
nano .env.production

# Start production services
docker-compose -f docker-compose.prod.yml up -d
```

### Production Commands
```bash
# Start production environment
docker-compose -f docker-compose.prod.yml up -d

# Scale backend services
docker-compose -f docker-compose.prod.yml up -d --scale backend=3

# View production logs
docker-compose -f docker-compose.prod.yml logs -f

# Update production deployment
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### SSL/TLS Setup
```bash
# Create SSL directory
mkdir -p nginx/ssl

# Generate self-signed certificate (for testing)
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/key.pem \
  -out nginx/ssl/cert.pem

# For production, use Let's Encrypt or your CA
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflows

#### 1. CI/CD Pipeline (`ci.yml`)
- Runs on push to `main` and `develop` branches
- Tests backend and frontend
- Security scanning with Trivy
- Builds and pushes Docker images
- Deploys to staging/production

#### 2. Docker Build and Test (`docker.yml`)
- Builds and tests Docker containers
- Security scanning of container images
- Pushes images to GitHub Container Registry

#### 3. Deployment (`deploy.yml`)
- Automated deployment after successful CI
- Environment-specific deployments
- Deployment notifications

### Workflow Triggers
```yaml
on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main, develop ]
  workflow_run:
    workflows: ["CI/CD Pipeline"]
    types: [completed]
```

### Environment Protection
- **Staging**: Deploys from `develop` branch
- **Production**: Deploys from `main` branch
- Requires manual approval for production

## 📊 Monitoring and Health Checks

### Health Check Endpoints
- **Backend**: `GET /health`
- **Frontend**: `GET /health`
- **Nginx**: `GET /health`

### Health Check Commands
```bash
# Check all services health
curl http://localhost:8000/health    # Backend
curl http://localhost:80/health      # Frontend

# Docker health status
docker-compose ps
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Health}}"
```

### Logging
```bash
# View all logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Follow logs in real-time
docker-compose logs -f --tail=100
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Port Conflicts
```bash
# Check what's using port 8000
netstat -tulpn | grep :8000

# Change ports in docker-compose.yml
ports:
  - "8001:8000"  # Map host port 8001 to container port 8000
```

#### 2. Container Won't Start
```bash
# Check container logs
docker-compose logs service_name

# Check container status
docker-compose ps

# Restart specific service
docker-compose restart service_name
```

#### 3. Database Connection Issues
```bash
# Check database container
docker-compose exec postgres psql -U webshop_user -d webshop

# Reset database
docker-compose down -v
docker-compose up -d
```

#### 4. Build Failures
```bash
# Clean build cache
docker-compose build --no-cache

# Remove all images and rebuild
docker-compose down --rmi all
docker-compose up --build
```

### Performance Optimization

#### 1. Resource Limits
```yaml
# In docker-compose.yml
services:
  backend:
    deploy:
      resources:
        limits:
          memory: 512M
          cpus: '0.5'
        reservations:
          memory: 256M
          cpus: '0.25'
```

#### 2. Multi-stage Builds
- Backend: Python builder + runtime stages
- Frontend: Node.js builder + Nginx runtime

#### 3. Layer Caching
```bash
# Use BuildKit for better caching
export DOCKER_BUILDKIT=1
docker-compose build
```

## 📚 Additional Resources

### Docker Commands Reference
```bash
# Container management
docker ps                    # List running containers
docker ps -a                # List all containers
docker stop <container>     # Stop container
docker rm <container>       # Remove container
docker logs <container>     # View container logs

# Image management
docker images               # List images
docker rmi <image>         # Remove image
docker pull <image>        # Pull image from registry
docker push <image>        # Push image to registry

# Volume management
docker volume ls            # List volumes
docker volume rm <volume>   # Remove volume
docker volume inspect <volume>  # Inspect volume
```

### Useful Scripts
```bash
# Quick restart
./scripts/restart.sh

# Clean up
./scripts/cleanup.sh

# Health check
./scripts/health-check.sh
```

### Support
- **Issues**: GitHub Issues
- **Documentation**: `/docs` directory
- **API Docs**: http://localhost:8000/docs (when running)

---

## 🎯 Next Steps

1. **Customize Environment Variables**: Update `.env` files for your environment
2. **Configure SSL**: Set up proper SSL certificates for production
3. **Set up Monitoring**: Configure logging and monitoring tools
4. **Scale Services**: Add load balancing and multiple backend instances
5. **Database Migration**: Migrate from SQLite to PostgreSQL for production
6. **Backup Strategy**: Implement database and file backup procedures

Your WebShop POC is now fully containerized and ready for CI/CD deployment! 🚀

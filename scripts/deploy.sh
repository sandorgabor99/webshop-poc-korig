#!/bin/bash

# WebShop POC Deployment Script
# Usage: ./scripts/deploy.sh [dev|staging|prod]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="webshop-poc"
BACKUP_DIR="./backups"
LOG_FILE="./deploy.log"

# Logging function
log() {
    echo -e "${BLUE}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

# Error function
error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

# Success function
success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$LOG_FILE"
}

# Warning function
warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# Check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        error "Docker is not running. Please start Docker and try again."
    fi
}

# Check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        error "Docker Compose is not installed. Please install Docker Compose and try again."
    fi
}

# Create backup
create_backup() {
    local env=$1
    local timestamp=$(date +'%Y%m%d_%H%M%S')
    local backup_file="${BACKUP_DIR}/${env}_${timestamp}.tar.gz"
    
    log "Creating backup for ${env} environment..."
    
    mkdir -p "$BACKUP_DIR"
    
    # Backup database and uploads
    if [ "$env" = "prod" ]; then
        docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U webshop_user webshop > "${BACKUP_DIR}/db_${timestamp}.sql"
        tar -czf "$backup_file" -C . uploads/ webshop.db "${BACKUP_DIR}/db_${timestamp}.sql"
    else
        tar -czf "$backup_file" -C . uploads/ webshop.db
    fi
    
    success "Backup created: $backup_file"
}

# Deploy function
deploy() {
    local env=$1
    local compose_file="docker-compose.yml"
    
    case $env in
        "dev")
            log "Deploying to development environment..."
            ;;
        "staging")
            log "Deploying to staging environment..."
            compose_file="docker-compose.staging.yml"
            ;;
        "prod")
            log "Deploying to production environment..."
            compose_file="docker-compose.prod.yml"
            create_backup "$env"
            ;;
        *)
            error "Invalid environment. Use: dev, staging, or prod"
            ;;
    esac
    
    # Check if compose file exists
    if [ ! -f "$compose_file" ]; then
        error "Docker Compose file not found: $compose_file"
    fi
    
    # Stop existing services
    log "Stopping existing services..."
    docker-compose -f "$compose_file" down --remove-orphans || true
    
    # Pull latest images
    log "Pulling latest images..."
    docker-compose -f "$compose_file" pull || true
    
    # Build and start services
    log "Building and starting services..."
    docker-compose -f "$compose_file" up --build -d
    
    # Wait for services to be ready
    log "Waiting for services to be ready..."
    sleep 30
    
    # Health check
    log "Performing health checks..."
    if [ "$env" = "prod" ]; then
        # Production health checks
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            success "Backend health check passed"
        else
            error "Backend health check failed"
        fi
        
        if curl -f http://localhost:80/health > /dev/null 2>&1; then
            success "Frontend health check passed"
        else
            error "Frontend health check failed"
        fi
    else
        # Development health checks
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            success "Backend health check passed"
        else
            error "Backend health check failed"
        fi
        
        if curl -f http://localhost:80/health > /dev/null 2>&1; then
            success "Frontend health check passed"
        else
            error "Frontend health check failed"
        fi
    fi
    
    success "Deployment to $env environment completed successfully!"
}

# Rollback function
rollback() {
    local env=$1
    local backup_file=$2
    
    if [ -z "$backup_file" ]; then
        error "Please specify a backup file to rollback to"
    fi
    
    if [ ! -f "$backup_file" ]; then
        error "Backup file not found: $backup_file"
    fi
    
    log "Rolling back to backup: $backup_file"
    
    # Stop services
    docker-compose -f docker-compose.prod.yml down
    
    # Extract backup
    tar -xzf "$backup_file"
    
    # Restart services
    docker-compose -f docker-compose.prod.yml up -d
    
    success "Rollback completed successfully!"
}

# Status function
status() {
    local env=${1:-"dev"}
    local compose_file="docker-compose.yml"
    
    case $env in
        "staging")
            compose_file="docker-compose.staging.yml"
            ;;
        "prod")
            compose_file="docker-compose.prod.yml"
            ;;
    esac
    
    log "Checking status of $env environment..."
    docker-compose -f "$compose_file" ps
}

# Main script
main() {
    local action=${1:-"deploy"}
    local environment=${2:-"dev"}
    
    log "Starting WebShop POC deployment script..."
    
    # Check prerequisites
    check_docker
    check_docker_compose
    
    case $action in
        "deploy")
            deploy "$environment"
            ;;
        "rollback")
            rollback "$environment" "$3"
            ;;
        "status")
            status "$environment"
            ;;
        "backup")
            create_backup "$environment"
            ;;
        *)
            echo "Usage: $0 [deploy|rollback|status|backup] [dev|staging|prod] [backup_file]"
            echo ""
            echo "Actions:"
            echo "  deploy    - Deploy the application (default)"
            echo "  rollback  - Rollback to a previous backup"
            echo "  status    - Show service status"
            echo "  backup    - Create a backup"
            echo ""
            echo "Environments:"
            echo "  dev       - Development environment (default)"
            echo "  staging   - Staging environment"
            echo "  prod      - Production environment"
            echo ""
            echo "Examples:"
            echo "  $0                    # Deploy to dev"
            echo "  $0 deploy staging     # Deploy to staging"
            echo "  $0 deploy prod        # Deploy to production"
            echo "  $0 status prod        # Check production status"
            echo "  $0 backup prod        # Create production backup"
            echo "  $0 rollback prod backup_file.tar.gz  # Rollback production"
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"

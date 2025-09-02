@echo off
setlocal enabledelayedexpansion

REM WebShop POC Deployment Script for Windows
REM Usage: deploy.bat [dev|staging|prod]

set PROJECT_NAME=webshop-poc
set BACKUP_DIR=.\backups
set LOG_FILE=.\deploy.log

REM Colors (Windows 10+)
set RED=[91m
set GREEN=[92m
set YELLOW=[93m
set BLUE=[94m
set NC=[0m

REM Logging function
:log
echo [%date% %time%] %~1 | tee -a "%LOG_FILE%"
goto :eof

REM Error function
:error
echo %RED%[ERROR]%NC% %~1 | tee -a "%LOG_FILE%"
exit /b 1

REM Success function
:success
echo %GREEN%[SUCCESS]%NC% %~1 | tee -a "%LOG_FILE%"
goto :eof

REM Warning function
:warning
echo %YELLOW%[WARNING]%NC% %~1 | tee -a "%LOG_FILE%"
goto :eof

REM Check if Docker is running
:check_docker
docker info >nul 2>&1
if errorlevel 1 (
    call :error "Docker is not running. Please start Docker and try again."
    exit /b 1
)
goto :eof

REM Check if Docker Compose is available
:check_docker_compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    call :error "Docker Compose is not installed. Please install Docker Compose and try again."
    exit /b 1
)
goto :eof

REM Create backup
:create_backup
set env=%~1
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "timestamp=%dt:~0,8%_%dt:~8,6%"
set "backup_file=%BACKUP_DIR%\%env%_%timestamp%.tar.gz"

call :log "Creating backup for %env% environment..."

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Backup database and uploads
if "%env%"=="prod" (
    docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U webshop_user webshop > "%BACKUP_DIR%\db_%timestamp%.sql"
    tar -czf "%backup_file%" -C . uploads/ webshop.db "%BACKUP_DIR%\db_%timestamp%.sql"
) else (
    tar -czf "%backup_file%" -C . uploads/ webshop.db
)

call :success "Backup created: %backup_file%"
goto :eof

REM Deploy function
:deploy
set env=%~1
set compose_file=docker-compose.yml

if "%env%"=="staging" set compose_file=docker-compose.staging.yml
if "%env%"=="prod" (
    set compose_file=docker-compose.prod.yml
    call :create_backup "%env%"
)

call :log "Deploying to %env% environment..."

REM Check if compose file exists
if not exist "%compose_file%" (
    call :error "Docker Compose file not found: %compose_file%"
    exit /b 1
)

REM Stop existing services
call :log "Stopping existing services..."
docker-compose -f "%compose_file%" down --remove-orphans

REM Pull latest images
call :log "Pulling latest images..."
docker-compose -f "%compose_file%" pull

REM Build and start services
call :log "Building and starting services..."
docker-compose -f "%compose_file%" up --build -d

REM Wait for services to be ready
call :log "Waiting for services to be ready..."
timeout /t 30 /nobreak >nul

REM Health check
call :log "Performing health checks..."
if "%env%"=="prod" (
    REM Production health checks
    curl -f http://localhost:8000/health >nul 2>&1
    if errorlevel 1 (
        call :error "Backend health check failed"
        exit /b 1
    ) else (
        call :success "Backend health check passed"
    )
    
    curl -f http://localhost:80/health >nul 2>&1
    if errorlevel 1 (
        call :error "Frontend health check failed"
        exit /b 1
    ) else (
        call :success "Frontend health check passed"
    )
) else (
    REM Development health checks
    curl -f http://localhost:8000/health >nul 2>&1
    if errorlevel 1 (
        call :error "Backend health check failed"
        exit /b 1
    ) else (
        call :success "Backend health check passed"
    )
    
    curl -f http://localhost:80/health >nul 2>&1
    if errorlevel 1 (
        call :error "Frontend health check failed"
        exit /b 1
    ) else (
        call :success "Frontend health check passed"
    )
)

call :success "Deployment to %env% environment completed successfully!"
goto :eof

REM Status function
:status
set env=%~1
if "%env%"=="" set env=dev
set compose_file=docker-compose.yml

if "%env%"=="staging" set compose_file=docker-compose.staging.yml
if "%env%"=="prod" set compose_file=docker-compose.prod.yml

call :log "Checking status of %env% environment..."
docker-compose -f "%compose_file%" ps
goto :eof

REM Main script
set action=%1
if "%action%"=="" set action=deploy

set environment=%2
if "%environment%"=="" set environment=dev

call :log "Starting WebShop POC deployment script..."

REM Check prerequisites
call :check_docker
call :check_docker_compose

if "%action%"=="deploy" (
    call :deploy "%environment%"
) else if "%action%"=="status" (
    call :status "%environment%"
) else if "%action%"=="backup" (
    call :create_backup "%environment%"
) else (
    echo Usage: %0 [deploy^|status^|backup] [dev^|staging^|prod]
    echo.
    echo Actions:
    echo   deploy    - Deploy the application ^(default^)
    echo   status    - Show service status
    echo   backup    - Create a backup
    echo.
    echo Environments:
    echo   dev       - Development environment ^(default^)
    echo   staging   - Staging environment
    echo   prod      - Production environment
    echo.
    echo Examples:
    echo   %0                    # Deploy to dev
    echo   %0 deploy staging     # Deploy to staging
    echo   %0 deploy prod        # Deploy to production
    echo   %0 status prod        # Check production status
    echo   %0 backup prod        # Create production backup
    exit /b 1
)

call :log "Deployment script completed successfully!"

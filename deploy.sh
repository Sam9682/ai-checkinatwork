#!/bin/bash
# AI Check-in at Work Production Deployment Script

# Handle command line arguments
COMMAND=${1:-help}
USER_ID=${2:-1}
USER_NAME=${3:-"User"}
USER_EMAIL=${4:-"user@example.com"}
DESCRIPTION=${5:-"Employee Check-in System"}

# Port configuration
APPLICATION_IDENTITY_NUMBER=6
RANGE_START=6000
RANGE_RESERVED=10
PORT_RANGE_BEGIN=$((APPLICATION_IDENTITY_NUMBER * 100 + RANGE_START))

set -e

echo "🚀 AI Check-in at Work Production Deployment"
echo "============================================"

# Configuration
DOMAIN=${DOMAIN:-"ai-checkin.swautomorph.com"}
EMAIL=${EMAIL:-"admin@swautomorph.com"}
ENV_FILE=".env.prod"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Helper functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -eq 0 ]]; then
   log_error "This script should not be run as root"
   exit 1
fi

# Check prerequisites
check_prerequisites() {
    log_info "Checking prerequisites..."
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose is not installed. Please install Docker Compose first."
        exit 1
    fi
    
    log_info "Prerequisites check passed ✅"
}

# Generate secure passwords
generate_secrets() {
    log_info "Generating secure secrets..."
    
    if [[ ! -f "$ENV_FILE" ]]; then
        log_info "Creating production environment file..."
        
        # Generate secure secret key
        SECRET_KEY=$(openssl rand -base64 32 | tr -d "=+/" | cut -c1-32)
        
        cat > "$ENV_FILE" << EOF
# Flask Configuration
SECRET_KEY=$SECRET_KEY
FLASK_ENV=production

# Domain Configuration
DOMAIN=$DOMAIN
SSL_EMAIL=$EMAIL

# Port Configuration
PORT=$((PORT_RANGE_BEGIN + USER_ID * RANGE_RESERVED))
HTTPS_PORT=$((PORT_RANGE_BEGIN + USER_ID * RANGE_RESERVED + 1))
HTTP_PORT=$((PORT_RANGE_BEGIN + USER_ID * RANGE_RESERVED + 2))
EOF
        
        chmod 600 "$ENV_FILE"
        log_info "Environment file created with secure passwords ✅"
    else
        log_warn "Environment file already exists, skipping generation"
    fi
}

# Setup SSL certificates
setup_ssl() {
    log_info "Setting up SSL certificates..."
    
    if [[ ! -d "ssl" ]]; then
        mkdir -p ssl
        
        # Check if certbot is installed
        if command -v certbot &> /dev/null; then
            log_info "Obtaining SSL certificate for $DOMAIN..."
            
            # Stop nginx if running
            sudo systemctl stop nginx 2>/dev/null || true
            
            # Get certificate
            sudo certbot certonly --standalone \
                -d "$DOMAIN" \
                --email "$EMAIL" \
                --agree-tos \
                --non-interactive \
                --quiet
            
            # Copy certificates
            sudo cp "/etc/letsencrypt/live/$DOMAIN/fullchain.pem" ssl/
            sudo cp "/etc/letsencrypt/live/$DOMAIN/privkey.pem" ssl/
            sudo chown -R $USER:$USER ssl/
            
            log_info "SSL certificates obtained ✅"
        else
            log_warn "Certbot not found. Creating self-signed certificates for testing..."
            
            # Create self-signed certificate for testing
            openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
                -keyout ssl/privkey.pem \
                -out ssl/fullchain.pem \
                -subj "/C=US/ST=State/L=City/O=Organization/CN=$DOMAIN"
            
            log_warn "Self-signed certificate created. Replace with real certificate for production!"
        fi
    else
        log_info "SSL directory already exists, skipping certificate generation"
    fi
}

# Create necessary directories
setup_directories() {
    log_info "Setting up directories..."
    
    mkdir -p data
    mkdir -p templates
    mkdir -p static/css
    mkdir -p static/js
    
    log_info "Directories created ✅"
}

# Build and deploy
deploy_services() {
    log_info "Building and deploying services..."
    
    # Load environment variables
    source "$ENV_FILE"
    
    # Stop existing services
    docker-compose down 2>/dev/null || true
    
    # Build images
    log_info "Building Docker images..."
    docker-compose build --no-cache
    
    # Start services
    log_info "Starting production services..."
    docker-compose --env-file "$ENV_FILE" up -d
    
    # Wait for services to be ready
    log_info "Waiting for services to start..."
    sleep 30
    
    # Check service health
    if docker-compose ps | grep -q "Up"; then
        log_info "Services deployed successfully ✅"
    else
        log_error "Some services failed to start"
        docker-compose logs
        exit 1
    fi
}

# Verify deployment
verify_deployment() {
    log_info "Verifying deployment..."
    
    # Check if services are running
    if ! docker-compose ps | grep -q "Up"; then
        log_error "Services are not running properly"
        return 1
    fi
    
    # Test application health
    sleep 10
    PORT=$((PORT_RANGE_BEGIN + USER_ID * RANGE_RESERVED))
    if curl -f -s "http://localhost:$PORT/" > /dev/null; then
        log_info "Application health check passed ✅"
    else
        log_warn "Application health check failed, but services are running"
    fi
    
    log_info "Deployment verification completed"
}

# Setup firewall
setup_firewall() {
    log_info "Configuring firewall..."
    
    if command -v ufw &> /dev/null; then
        # Configure UFW if available
        PORT=$((PORT_RANGE_BEGIN + USER_ID * RANGE_RESERVED))
        HTTPS_PORT=$((PORT_RANGE_BEGIN + USER_ID * RANGE_RESERVED + 1))
        HTTP_PORT=$((PORT_RANGE_BEGIN + USER_ID * RANGE_RESERVED + 2))
        
        sudo ufw allow $PORT/tcp
        sudo ufw allow $HTTPS_PORT/tcp
        sudo ufw allow $HTTP_PORT/tcp
        
        log_info "Firewall configured ✅"
    else
        log_warn "UFW not found, skipping firewall configuration"
    fi
}

# Create backup script
create_backup_script() {
    log_info "Creating backup script..."
    
    cat > backup.sh << 'EOF'
#!/bin/bash
# AI Check-in at Work Backup Script

BACKUP_DIR="backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/checkin_backup_$DATE"

mkdir -p "$BACKUP_DIR"

echo "Creating backup: $BACKUP_FILE"
docker-compose exec -T checkin-app cp /app/data/checkin_system.db /tmp/backup.db
docker cp $(docker-compose ps -q checkin-app):/tmp/backup.db "$BACKUP_FILE.db"

if [[ $? -eq 0 ]]; then
    echo "Backup created successfully: $BACKUP_FILE"
    
    # Keep only last 7 backups
    ls -t "$BACKUP_DIR"/checkin_backup_*.db | tail -n +8 | xargs -r rm
    echo "Old backups cleaned up"
else
    echo "Backup failed!"
    exit 1
fi
EOF
    
    chmod +x backup.sh
    log_info "Backup script created ✅"
}

# Main deployment process
main() {
    log_info "Starting AI Check-in at Work production deployment..."
    
    check_prerequisites
    generate_secrets
    setup_ssl
    setup_directories
    deploy_services
    verify_deployment
    setup_firewall
    create_backup_script
    
    echo ""
    echo "🎉 Deployment completed successfully!"
    echo "===================================="
    echo "🌐 Web Interface: https://$DOMAIN"
    echo "🔑 Demo Login: admin / admin123"
    echo ""
    echo "📋 Next Steps:"
    echo "1. Test the application at https://$DOMAIN"
    echo "2. Change default admin password"
    echo "3. Configure DNS to point to this server"
    echo "4. Set up automated backups: ./backup.sh"
    echo "5. Monitor logs: docker-compose logs -f"
    echo ""
    echo "🔧 Management Commands:"
    echo "- View logs: docker-compose logs -f"
    echo "- Backup database: ./backup.sh"
    echo "- Stop services: ./deploy.sh stop"
    echo "- Restart services: ./deploy.sh restart"
}

# Stop services
stop_services() {
    log_info "Stopping AI Check-in at Work services..."
    docker-compose down
    log_info "Services stopped successfully ✅"
}

# Restart services
restart_services() {
    log_info "Restarting AI Check-in at Work services..."
    docker-compose restart
    log_info "Services restarted successfully ✅"
}

# Check service status
check_status() {
    log_info "Checking AI Check-in at Work service status..."
    echo ""
    docker-compose ps
    echo ""
    
    if docker-compose ps | grep -q "Up"; then
        log_info "AI Check-in at Work is running ✅"
    else
        log_warn "AI Check-in at Work is not running ⚠️"
    fi
}

# Show logs
show_logs() {
    log_info "Showing AI Check-in at Work logs..."
    docker-compose logs -f
}

# Handle script arguments
case "${1:-help}" in
    "start")
        main
        ;;
    "ssl")
        setup_ssl
        ;;
    "backup")
        create_backup_script
        ./backup.sh
        ;;
    "verify")
        verify_deployment
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        restart_services
        ;;
    "ps")
        check_status
        ;;
    "logs")
        show_logs
        ;;
    "help")
        echo "Usage: $0 [start|ssl|backup|verify|stop|restart|ps|logs|help]"
        echo "  start   - Full production deployment"
        echo "  ssl     - Setup SSL certificates only"
        echo "  backup  - Create database backup"
        echo "  verify  - Verify deployment status"
        echo "  stop    - Stop all services"
        echo "  restart - Restart all services"
        echo "  ps      - Check service status"
        echo "  logs    - Show application logs"
        echo "  help    - Show this help message (default)"
        ;;
    *)
        echo "Usage: $0 [start|ssl|backup|verify|stop|restart|ps|logs|help]"
        exit 1
        ;;
esac
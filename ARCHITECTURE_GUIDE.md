# Architecture Guide

## Application Architecture

### Core Components

```
ai-checkinatwork/
├── src/                    # Application source code
│   ├── config.py          # Configuration settings
│   ├── models/            # Data models
│   ├── routes/            # API endpoints
│   └── templates/         # HTML templates
├── static/                # Static assets (CSS, JS)
├── data/                  # Database files
├── requirements.txt       # Python dependencies
├── main.py               # Application entry point
├── Dockerfile            # Container definition
├── docker-compose.yml    # Service orchestration
├── deploy.sh            # Deployment automation
└── deploy.ini           # Deployment configuration
```

### Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML/CSS/JavaScript
- **Containerization**: Docker + Docker Compose
- **Deployment**: Automated via deploy.sh script

## Standardized Deployment Architecture

### Universal Components

#### 1. docker-compose.yml
Orchestrates all services with consistent structure:
```yaml
version: '3.8'
services:
  app:
    build: .
    ports:
      - "${APP_PORT}:5000"
    environment:
      - FLASK_ENV=${ENVIRONMENT}
    volumes:
      - ./data:/app/data
  
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

#### 2. deploy.sh (Universal Script)
Single script for all applications with commands:
- `./deploy.sh start` - Initialize and start services
- `./deploy.sh stop` - Stop all services
- `./deploy.sh restart` - Restart services
- `./deploy.sh backup` - Backup application data
- `./deploy.sh logs` - View service logs

#### 3. deploy.ini (Application-Specific)
Configuration file customized per application:
```ini
[app]
name=ai-checkinatwork
port=5000
domain=ai-checkin.swautomorph.com

[database]
type=sqlite
backup_enabled=true

[ssl]
enabled=true
email=admin@swautomorph.com
```

## Q Chat GenAI Integration

### Automated Evolution Process

#### 1. Code Analysis
Q Chat GenAI analyzes existing codebase to understand:
- Current architecture patterns
- Dependencies and configurations
- Business logic and data models

#### 2. Feature Development
- Generates new features based on requirements
- Maintains consistency with existing code style
- Updates configuration files automatically

#### 3. Deployment Automation
- Modifies `deploy.ini` for new requirements
- Updates `docker-compose.yml` if needed
- Maintains `deploy.sh` compatibility

### Standardization Benefits

#### Consistency Across Applications
- Same deployment commands for all projects
- Uniform configuration structure
- Predictable service architecture

#### Rapid Development
- Q Chat GenAI understands standard patterns
- Faster feature implementation
- Automated configuration updates

#### Simplified Operations
- Single script manages entire lifecycle
- Consistent backup and monitoring
- Standardized SSL and domain setup

## Implementation Flow

### New Application Setup
1. Copy standard `deploy.sh` script
2. Create application-specific `deploy.ini`
3. Implement `docker-compose.yml` with standard structure
4. Q Chat GenAI generates application code following patterns

### Feature Evolution
1. Q Chat GenAI analyzes current state
2. Implements new features maintaining architecture
3. Updates configurations as needed
4. Deploy using standard `./deploy.sh restart`

### Production Deployment
1. Configure `deploy.ini` with production settings
2. Run `./deploy.sh start` for automated setup
3. SSL certificates and domain configuration handled automatically
4. Monitoring and backup systems activated

## Security & Best Practices

### Container Security
- Non-root user execution
- Minimal base images
- Environment variable configuration

### Data Protection
- Automated backups via deploy.sh
- Volume mounting for persistence
- SSL/TLS encryption in production

### Configuration Management
- Environment-specific settings in deploy.ini
- Secrets management through environment variables
- Centralized configuration validation

This architecture enables rapid development and deployment of similar applications while maintaining consistency and leveraging Q Chat GenAI for automated evolution and maintenance.
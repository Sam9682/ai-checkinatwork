# AI Check-in at Work

Employee check-in timing management system built with Flask, following the same architecture as the AI-HACCP project.

## Features

- Employee authentication and login
- Real-time check-in/check-out functionality
- Attendance tracking and history
- Late arrival detection
- Dashboard with current status
- Responsive web interface
- Docker deployment with SSL support

## Quick Start

### Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

3. Access at http://localhost:5000

### Production Deployment

1. Make the deploy script executable:
```bash
chmod +x deploy.sh
```

2. Start full deployment:
```bash
./deploy.sh start
```

3. Access at https://ai-checkin.swautomorph.com

## Default Login

- Username: `admin`
- Password: `admin123`

## Management Commands

- `./deploy.sh start` - Full production deployment
- `./deploy.sh stop` - Stop all services
- `./deploy.sh restart` - Restart services
- `./deploy.sh ps` - Check service status
- `./deploy.sh backup` - Create database backup
- `./deploy.sh ssl` - Setup SSL certificates only

## Configuration

Work schedule settings can be configured in `src/config.py`:

- `WORK_START_TIME` - Standard work start time (default: 09:00)
- `WORK_END_TIME` - Standard work end time (default: 17:00)
- `LATE_THRESHOLD_MINUTES` - Minutes after start time to mark as late (default: 15)

## Architecture

- **Backend**: Flask with SQLite database
- **Frontend**: Bootstrap-based responsive templates
- **Deployment**: Docker with Nginx reverse proxy
- **SSL**: Let's Encrypt certificates with automatic renewal

## Database Schema

- **employees**: Employee information and credentials
- **checkins**: Daily check-in/check-out records
- **work_schedules**: Employee work schedule configuration

## API Endpoints

- `POST /checkin` - Record check-in time
- `POST /checkout` - Record check-out time
- `GET /api/status` - Get current check-in status (JSON)

## Security Features

- Secure password hashing
- Session-based authentication
- HTTPS encryption
- Environment-based configuration
- Input validation and sanitization
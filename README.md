# AI Check-in at Work

Employee check-in timing management system built with Flask, following the same architecture as the AI-HACCP project.

## Features

- Employee authentication and login
- Real-time check-in/check-out functionality
- Attendance tracking and history
- Late arrival detection
- Dashboard with current status
- **Billing and cost tracking system**
- **Time-based cost calculation with configurable hourly rates**
- **Detailed billing reports with period selection**
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
# OR use the development runner
python run_dev.py
```

3. Access at http://localhost:5000
   - Dashboard: http://localhost:5000
   - Billing Report: http://localhost:5000/billing

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
- Default hourly rate: $25.00

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
- `DEFAULT_HOURLY_RATE` - Default hourly billing rate (default: $25.00)

## Architecture

- **Backend**: Flask with SQLite database
- **Frontend**: Bootstrap-based responsive templates
- **Deployment**: Docker with Nginx reverse proxy
- **SSL**: Let's Encrypt certificates with automatic renewal

## Database Schema

- **employees**: Employee information and credentials
- **checkins**: Daily check-in/check-out records
- **work_schedules**: Employee work schedule configuration
- **billing_rates**: Employee hourly rates and billing configuration

## API Endpoints

- `POST /checkin` - Record check-in time
- `POST /checkout` - Record check-out time
- `GET /api/status` - Get current check-in status (JSON)
- `GET /billing` - View billing reports and cost analysis

## Billing System

The billing system calculates costs based on actual work hours:

- **Automatic calculation**: Hours worked = check-out time - check-in time
- **Configurable rates**: Each employee can have different hourly rates
- **Period reports**: View costs for current month, last month, or custom periods
- **Detailed breakdown**: Daily records with hours worked and costs
- **Summary metrics**: Total hours, total cost, average daily hours

### Billing Features

- Real-time cost calculation based on check-in/check-out times
- Monthly and custom period reporting
- Hourly rate management per employee
- Export-ready detailed billing records
- Visual summary cards with key metrics

## Security Features

- Secure password hashing
- Session-based authentication
- HTTPS encryption
- Environment-based configuration
- Input validation and sanitization
# AI Check-in at Work

## Objective

Employee attendance tracking system with billing capabilities. Tracks check-in/check-out times, calculates work hours, generates cost reports, and provides admin user management.

## Installation & Configuration

### Prerequisites
- Python 3.8+
- Docker (for production)

### Development Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

Access: http://localhost:5000

### Production Setup

```bash
# Deploy with Docker
chmod +x deploy.sh
./deploy.sh start
```

Access: https://ai-checkin.swautomorph.com

### Default Credentials
- Username: `admin`
- Password: `password`

### Configuration

Edit `src/config.py`:

```python
WORK_START_TIME = "09:00"          # Work start time
WORK_END_TIME = "17:00"            # Work end time  
LATE_THRESHOLD_MINUTES = 15        # Late arrival threshold
DEFAULT_HOURLY_RATE = 25.00       # Default billing rate
```

### Key Endpoints

- `/` - Dashboard
- `/checkin` - Check-in (POST)
- `/checkout` - Check-out (POST)
- `/billing` - Billing reports
- `/admin/users` - User management (admin only)
- `/api/status` - Status API (JSON)

### Management Commands

```bash
./deploy.sh start     # Start services
./deploy.sh stop      # Stop services
./deploy.sh restart   # Restart services
./deploy.sh backup    # Backup database
```
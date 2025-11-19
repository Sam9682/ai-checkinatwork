"""Configuration settings for AI Check-in at Work"""
import os

# Database configuration
DB_PATH = 'checkin_system.db'

# Flask configuration
SECRET_KEY = os.environ.get('SECRET_KEY', 'checkin-secret-key-change-in-production')
FLASK_ENV = os.environ.get('FLASK_ENV', 'development')

# CORS configuration
CORS_ORIGINS = ['*']

# Check-in settings
WORK_START_TIME = "09:00"
WORK_END_TIME = "17:00"
LATE_THRESHOLD_MINUTES = 15
EARLY_LEAVE_THRESHOLD_MINUTES = 30

# Language translations
TRANSLATIONS = {
    'en': {
        'login': 'Login',
        'register': 'Register',
        'username': 'Username',
        'email': 'Email',
        'password': 'Password',
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'dashboard': 'Dashboard',
        'logout': 'Logout',
        'welcome': 'Welcome',
        'check_in': 'Check In',
        'check_out': 'Check Out',
        'status': 'Status',
        'time': 'Time',
        'employee_id': 'Employee ID',
        'department': 'Department',
        'today_status': "Today's Status",
        'attendance_history': 'Attendance History',
        'late': 'Late',
        'on_time': 'On Time',
        'early_leave': 'Early Leave',
        'present': 'Present',
        'absent': 'Absent'
    }
}
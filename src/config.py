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

# Billing settings
DEFAULT_HOURLY_RATE = 25.0  # Default hourly rate in USD

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
        'attendance_history': 'Recent Attendance',
        'late': 'Late',
        'on_time': 'On Time',
        'early_leave': 'Early Leave',
        'present': 'Present',
        'absent': 'Absent',
        'current_time': 'Current Time',
        'employee_login': 'Employee Login',
        'not_checked_in': 'Not checked in',
        'not_checked_out': 'Not checked out',
        'no_checkin_today': 'No check-in record for today.',
        'work_day_complete': 'You have completed your work day!',
        'no_attendance_records': 'No attendance records found.',
        'date': 'Date',
        'admin_panel': 'Admin Panel',
        'delete_record': 'Delete Record',
        'purge_all': 'Purge All Records',
        'confirm_delete': 'Are you sure you want to delete this record?',
        'confirm_purge': 'Are you sure you want to delete ALL records? This cannot be undone!',
        'billing': 'Billing',
        'billing_report': 'Billing Report',
        'hours_worked': 'Hours Worked',
        'hourly_rate': 'Hourly Rate',
        'total_cost': 'Total Cost',
        'period': 'Period',
        'this_month': 'This Month',
        'last_month': 'Last Month',
        'custom_period': 'Custom Period',
        'from_date': 'From Date',
        'to_date': 'To Date',
        'generate_report': 'Generate Report',
        'no_billing_data': 'No billing data found for the selected period.'
    },
    'fr': {
        'login': 'Connexion',
        'register': 'Inscription',
        'username': "Nom d'utilisateur",
        'email': 'Email',
        'password': 'Mot de passe',
        'first_name': 'Prénom',
        'last_name': 'Nom',
        'dashboard': 'Tableau de bord',
        'logout': 'Déconnexion',
        'welcome': 'Bienvenue',
        'check_in': 'Pointer',
        'check_out': 'Dépointer',
        'status': 'Statut',
        'time': 'Heure',
        'employee_id': 'ID Employé',
        'department': 'Département',
        'today_status': "Statut d'aujourd'hui",
        'attendance_history': 'Présences récentes',
        'late': 'En retard',
        'on_time': 'À l\'heure',
        'early_leave': 'Départ anticipé',
        'present': 'Présent',
        'absent': 'Absent',
        'current_time': 'Heure actuelle',
        'employee_login': 'Connexion employé',
        'not_checked_in': 'Pas encore pointé',
        'not_checked_out': 'Pas encore dépointé',
        'no_checkin_today': "Aucun pointage aujourd'hui.",
        'work_day_complete': 'Vous avez terminé votre journée de travail !',
        'no_attendance_records': 'Aucun enregistrement de présence trouvé.',
        'date': 'Date',
        'admin_panel': 'Panneau d\'administration',
        'delete_record': 'Supprimer l\'enregistrement',
        'purge_all': 'Purger tous les enregistrements',
        'confirm_delete': 'Êtes-vous sûr de vouloir supprimer cet enregistrement ?',
        'confirm_purge': 'Êtes-vous sûr de vouloir supprimer TOUS les enregistrements ? Cette action est irréversible !',
        'billing': 'Facturation',
        'billing_report': 'Rapport de facturation',
        'hours_worked': 'Heures travaillées',
        'hourly_rate': 'Taux horaire',
        'total_cost': 'Coût total',
        'period': 'Période',
        'this_month': 'Ce mois',
        'last_month': 'Mois dernier',
        'custom_period': 'Période personnalisée',
        'from_date': 'Date de début',
        'to_date': 'Date de fin',
        'generate_report': 'Générer le rapport',
        'no_billing_data': 'Aucune donnée de facturation trouvée pour la période sélectionnée.'
    }
}
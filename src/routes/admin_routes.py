"""Admin management routes"""
from flask import Blueprint, request, redirect, url_for, session, flash, render_template
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta
from calendar import monthrange
from ..database import get_db_connection
from ..config import DEFAULT_HOURLY_RATE

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """Decorator to require admin access"""
    def decorated_function(*args, **kwargs):
        if 'employee_id' not in session or session.get('username') != 'admin':
            flash('Admin access required')
            return redirect(url_for('main.dashboard'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@admin_bp.route('/admin')
@admin_required
def admin_panel():
    conn = get_db_connection()
    
    # Get all check-in records
    all_checkins = conn.execute('''
        SELECT c.*, e.first_name, e.last_name, e.employee_id as emp_id
        FROM checkins c
        JOIN employees e ON c.employee_id = e.id
        ORDER BY c.date DESC, c.check_in_time DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin_panel.html', checkins=all_checkins)

@admin_bp.route('/admin/delete/<int:checkin_id>', methods=['POST'])
@admin_required
def delete_checkin(checkin_id):
    conn = get_db_connection()
    
    conn.execute('DELETE FROM checkins WHERE id = ?', (checkin_id,))
    conn.commit()
    conn.close()
    
    flash('Check-in record deleted successfully')
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/purge', methods=['POST'])
@admin_required
def purge_all():
    conn = get_db_connection()
    
    conn.execute('DELETE FROM checkins')
    conn.commit()
    conn.close()
    
    flash('All check-in records have been purged')
    return redirect(url_for('admin.admin_panel'))

@admin_bp.route('/admin/users')
@admin_required
def manage_users():
    """Display user management page"""
    conn = get_db_connection()
    
    users = conn.execute('''
        SELECT e.id, e.employee_id, e.username, e.email, e.first_name, e.last_name, 
               e.department, e.position, e.is_active, e.created_at,
               br.hourly_rate
        FROM employees e
        LEFT JOIN billing_rates br ON e.id = br.employee_id AND br.is_active = 1
        ORDER BY e.created_at DESC
    ''').fetchall()
    
    conn.close()
    
    return render_template('admin/users.html', users=users)

@admin_bp.route('/admin/users/create', methods=['GET', 'POST'])
@admin_required
def create_user():
    """Create new user"""
    if request.method == 'POST':
        conn = get_db_connection()
        
        # Get form data
        employee_id = request.form['employee_id']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        position = request.form['position']
        hourly_rate = float(request.form.get('hourly_rate', DEFAULT_HOURLY_RATE))
        
        # Check if username or email exists
        existing = conn.execute(
            'SELECT id FROM employees WHERE username = ? OR email = ?',
            (username, email)
        ).fetchone()
        
        if existing:
            flash('Username or email already exists')
            conn.close()
            return redirect(url_for('admin.create_user'))
        
        # Create user
        password_hash = generate_password_hash(password)
        cursor = conn.execute('''
            INSERT INTO employees (employee_id, username, email, password_hash, first_name, last_name, department, position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (employee_id, username, email, password_hash, first_name, last_name, department, position))
        
        user_id = cursor.lastrowid
        
        # Create billing rate
        conn.execute('''
            INSERT INTO billing_rates (employee_id, hourly_rate, effective_date)
            VALUES (?, ?, ?)
        ''', (user_id, hourly_rate, date.today()))
        
        conn.commit()
        conn.close()
        
        flash(f'User {username} created successfully')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/create_user.html')

@admin_bp.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def edit_user(user_id):
    """Edit existing user"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        # Update user
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        department = request.form['department']
        position = request.form['position']
        is_active = 1 if request.form.get('is_active') else 0
        hourly_rate = float(request.form.get('hourly_rate', DEFAULT_HOURLY_RATE))
        
        conn.execute('''
            UPDATE employees 
            SET email = ?, first_name = ?, last_name = ?, department = ?, position = ?, is_active = ?
            WHERE id = ?
        ''', (email, first_name, last_name, department, position, is_active, user_id))
        
        # Update billing rate
        conn.execute('''
            UPDATE billing_rates 
            SET hourly_rate = ?
            WHERE employee_id = ? AND is_active = 1
        ''', (hourly_rate, user_id))
        
        conn.commit()
        conn.close()
        
        flash('User updated successfully')
        return redirect(url_for('admin.manage_users'))
    
    # Get user data
    user = conn.execute('''
        SELECT e.*, br.hourly_rate
        FROM employees e
        LEFT JOIN billing_rates br ON e.id = br.employee_id AND br.is_active = 1
        WHERE e.id = ?
    ''', (user_id,)).fetchone()
    
    conn.close()
    
    if not user:
        flash('User not found')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/edit_user.html', user=user)

@admin_bp.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def delete_user(user_id):
    """Delete user"""
    conn = get_db_connection()
    
    # Check if user exists and is not admin
    user = conn.execute('SELECT username FROM employees WHERE id = ?', (user_id,)).fetchone()
    
    if not user:
        flash('User not found')
    elif user['username'] == 'admin':
        flash('Cannot delete admin user')
    else:
        # Delete user and related data
        conn.execute('DELETE FROM billing_rates WHERE employee_id = ?', (user_id,))
        conn.execute('DELETE FROM checkins WHERE employee_id = ?', (user_id,))
        conn.execute('DELETE FROM employees WHERE id = ?', (user_id,))
        conn.commit()
        flash('User deleted successfully')
    
    conn.close()
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/admin/reports')
@admin_required
def reports():
    """Display activity reports"""
    conn = get_db_connection()
    
    # Get period from request
    period = request.args.get('period', 'week')
    
    if period == 'day':
        activity_data = get_daily_activity(conn)
    elif period == 'month':
        activity_data = get_monthly_activity(conn)
    else:  # week
        activity_data = get_weekly_activity(conn)
    
    conn.close()
    
    return render_template('admin/reports.html', 
                         activity_data=activity_data,
                         period=period)

def get_daily_activity(conn):
    """Get today's activity"""
    today = date.today()
    
    activities = conn.execute('''
        SELECT e.username, e.first_name, e.last_name,
               c.check_in_time, c.check_out_time, c.status
        FROM employees e
        LEFT JOIN checkins c ON e.id = c.employee_id AND c.date = ?
        WHERE e.is_active = 1
        ORDER BY e.username
    ''', (today,)).fetchall()
    
    return {
        'title': f'Daily Activity - {today}',
        'activities': activities
    }

def get_weekly_activity(conn):
    """Get this week's activity"""
    today = date.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)
    
    activities = conn.execute('''
        SELECT e.username, e.first_name, e.last_name,
               COUNT(c.id) as days_worked,
               COUNT(CASE WHEN c.status = 'late' THEN 1 END) as late_days,
               COUNT(CASE WHEN c.check_in_time IS NOT NULL THEN 1 END) as check_ins
        FROM employees e
        LEFT JOIN checkins c ON e.id = c.employee_id 
            AND c.date BETWEEN ? AND ?
        WHERE e.is_active = 1
        GROUP BY e.id, e.username, e.first_name, e.last_name
        ORDER BY e.username
    ''', (week_start, week_end)).fetchall()
    
    return {
        'title': f'Weekly Activity - {week_start} to {week_end}',
        'activities': activities,
        'is_summary': True
    }

def get_monthly_activity(conn):
    """Get this month's activity"""
    today = date.today()
    month_start = date(today.year, today.month, 1)
    month_end = date(today.year, today.month, monthrange(today.year, today.month)[1])
    
    activities = conn.execute('''
        SELECT e.username, e.first_name, e.last_name,
               COUNT(c.id) as days_worked,
               COUNT(CASE WHEN c.status = 'late' THEN 1 END) as late_days,
               COUNT(CASE WHEN c.check_in_time IS NOT NULL THEN 1 END) as check_ins,
               ROUND(AVG(CASE 
                   WHEN c.check_in_time IS NOT NULL AND c.check_out_time IS NOT NULL 
                   THEN (julianday(c.check_out_time) - julianday(c.check_in_time)) * 24 
               END), 2) as avg_hours
        FROM employees e
        LEFT JOIN checkins c ON e.id = c.employee_id 
            AND c.date BETWEEN ? AND ?
        WHERE e.is_active = 1
        GROUP BY e.id, e.username, e.first_name, e.last_name
        ORDER BY e.username
    ''', (month_start, month_end)).fetchall()
    
    return {
        'title': f'Monthly Activity - {month_start.strftime("%B %Y")}',
        'activities': activities,
        'is_summary': True,
        'show_hours': True
    }
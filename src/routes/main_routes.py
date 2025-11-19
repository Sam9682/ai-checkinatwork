"""Main application routes"""
from flask import Blueprint, render_template, session, redirect, url_for
from ..database import get_db_connection
from datetime import datetime, date

main_bp = Blueprint('main', __name__)

def login_required(f):
    """Decorator to require login"""
    def decorated_function(*args, **kwargs):
        if 'employee_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@main_bp.route('/')
def index():
    if 'employee_id' in session:
        return redirect(url_for('main.dashboard'))
    return redirect(url_for('auth.login'))

@main_bp.route('/dashboard')
@login_required
def dashboard():
    conn = get_db_connection()
    
    # Get today's check-in status
    today = date.today()
    checkin_today = conn.execute(
        'SELECT * FROM checkins WHERE employee_id = ? AND date = ?',
        (session['employee_id'], today)
    ).fetchone()
    
    # Get recent check-ins (last 7 days)
    recent_checkins = conn.execute('''
        SELECT * FROM checkins 
        WHERE employee_id = ? 
        ORDER BY date DESC 
        LIMIT 7
    ''', (session['employee_id'],)).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         checkin_today=checkin_today,
                         recent_checkins=recent_checkins)
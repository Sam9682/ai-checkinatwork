"""Check-in/Check-out routes"""
from flask import Blueprint, request, redirect, url_for, session, flash, jsonify
from datetime import datetime, date, time
from ..database import get_db_connection
from ..config import WORK_START_TIME, LATE_THRESHOLD_MINUTES

checkin_bp = Blueprint('checkin', __name__)

def login_required(f):
    """Decorator to require login"""
    def decorated_function(*args, **kwargs):
        if 'employee_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@checkin_bp.route('/checkin', methods=['POST'])
@login_required
def check_in():
    conn = get_db_connection()
    today = date.today()
    now = datetime.now()
    
    # Check if already checked in today
    existing = conn.execute(
        'SELECT * FROM checkins WHERE employee_id = ? AND date = ?',
        (session['employee_id'], today)
    ).fetchone()
    
    if existing and existing['check_in_time']:
        flash('Already checked in today')
        conn.close()
        return redirect(url_for('main.dashboard'))
    
    # Determine status (late/on-time)
    work_start = datetime.strptime(WORK_START_TIME, '%H:%M').time()
    current_time = now.time()
    
    status = 'on_time'
    if current_time > work_start:
        # Calculate minutes late
        start_datetime = datetime.combine(today, work_start)
        current_datetime = datetime.combine(today, current_time)
        minutes_late = (current_datetime - start_datetime).total_seconds() / 60
        
        if minutes_late > LATE_THRESHOLD_MINUTES:
            status = 'late'
    
    # Insert or update check-in
    if existing:
        conn.execute(
            'UPDATE checkins SET check_in_time = ?, status = ? WHERE id = ?',
            (now, status, existing['id'])
        )
    else:
        conn.execute(
            'INSERT INTO checkins (employee_id, check_in_time, date, status) VALUES (?, ?, ?, ?)',
            (session['employee_id'], now, today, status)
        )
    
    conn.commit()
    conn.close()
    
    flash(f'Checked in successfully at {now.strftime("%H:%M")}')
    return redirect(url_for('main.dashboard'))

@checkin_bp.route('/checkout', methods=['POST'])
@login_required
def check_out():
    conn = get_db_connection()
    today = date.today()
    now = datetime.now()
    
    # Get today's check-in record
    checkin_record = conn.execute(
        'SELECT * FROM checkins WHERE employee_id = ? AND date = ?',
        (session['employee_id'], today)
    ).fetchone()
    
    if not checkin_record or not checkin_record['check_in_time']:
        flash('Must check in first')
        conn.close()
        return redirect(url_for('main.dashboard'))
    
    if checkin_record['check_out_time']:
        flash('Already checked out today')
        conn.close()
        return redirect(url_for('main.dashboard'))
    
    # Update check-out time
    conn.execute(
        'UPDATE checkins SET check_out_time = ? WHERE id = ?',
        (now, checkin_record['id'])
    )
    
    conn.commit()
    conn.close()
    
    flash(f'Checked out successfully at {now.strftime("%H:%M")}')
    return redirect(url_for('main.dashboard'))

@checkin_bp.route('/api/status')
@login_required
def api_status():
    """API endpoint for current status"""
    conn = get_db_connection()
    today = date.today()
    
    checkin_today = conn.execute(
        'SELECT * FROM checkins WHERE employee_id = ? AND date = ?',
        (session['employee_id'], today)
    ).fetchone()
    
    conn.close()
    
    status = {
        'checked_in': bool(checkin_today and checkin_today['check_in_time']),
        'checked_out': bool(checkin_today and checkin_today['check_out_time']),
        'check_in_time': checkin_today['check_in_time'] if checkin_today else None,
        'check_out_time': checkin_today['check_out_time'] if checkin_today else None,
        'status': checkin_today['status'] if checkin_today else None
    }
    
    return jsonify(status)
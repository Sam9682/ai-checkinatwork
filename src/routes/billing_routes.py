"""Billing and reporting routes"""
from flask import Blueprint, request, render_template, session, redirect, url_for
from datetime import datetime, date, timedelta
from calendar import monthrange
from ..database import get_db_connection

billing_bp = Blueprint('billing', __name__)

def login_required(f):
    """Decorator to require login"""
    def decorated_function(*args, **kwargs):
        if 'employee_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@billing_bp.route('/billing')
@login_required
def billing_report():
    """Display billing report page"""
    conn = get_db_connection()
    
    # Get current month data by default
    today = date.today()
    start_date = date(today.year, today.month, 1)
    end_date = date(today.year, today.month, monthrange(today.year, today.month)[1])
    
    # Get period from request
    period = request.args.get('period', 'this_month')
    custom_start = request.args.get('start_date')
    custom_end = request.args.get('end_date')
    
    if period == 'last_month':
        if today.month == 1:
            start_date = date(today.year - 1, 12, 1)
            end_date = date(today.year - 1, 12, 31)
        else:
            start_date = date(today.year, today.month - 1, 1)
            end_date = date(today.year, today.month - 1, monthrange(today.year, today.month - 1)[1])
    elif period == 'custom' and custom_start and custom_end:
        start_date = datetime.strptime(custom_start, '%Y-%m-%d').date()
        end_date = datetime.strptime(custom_end, '%Y-%m-%d').date()
    
    # Get billing data
    billing_data = get_billing_data(conn, session['employee_id'], start_date, end_date)
    
    # Get current hourly rate
    current_rate = conn.execute('''
        SELECT hourly_rate FROM billing_rates 
        WHERE employee_id = ? AND is_active = 1 
        ORDER BY effective_date DESC LIMIT 1
    ''', (session['employee_id'],)).fetchone()
    
    hourly_rate = current_rate['hourly_rate'] if current_rate else 25.00
    
    conn.close()
    
    return render_template('billing.html', 
                         billing_data=billing_data,
                         hourly_rate=hourly_rate,
                         period=period,
                         start_date=start_date,
                         end_date=end_date,
                         custom_start=custom_start,
                         custom_end=custom_end)

def get_billing_data(conn, employee_id, start_date, end_date):
    """Calculate billing data for the given period"""
    checkins = conn.execute('''
        SELECT date, check_in_time, check_out_time, status
        FROM checkins 
        WHERE employee_id = ? AND date BETWEEN ? AND ?
        AND check_in_time IS NOT NULL AND check_out_time IS NOT NULL
        ORDER BY date
    ''', (employee_id, start_date, end_date)).fetchall()
    
    billing_records = []
    total_hours = 0
    total_cost = 0
    
    # Get hourly rate for the period
    rate_record = conn.execute('''
        SELECT hourly_rate FROM billing_rates 
        WHERE employee_id = ? AND effective_date <= ? AND is_active = 1
        ORDER BY effective_date DESC LIMIT 1
    ''', (employee_id, end_date)).fetchone()
    
    hourly_rate = rate_record['hourly_rate'] if rate_record else 25.00
    
    for checkin in checkins:
        if checkin['check_in_time'] and checkin['check_out_time']:
            # Parse datetime strings
            check_in = datetime.strptime(checkin['check_in_time'], '%Y-%m-%d %H:%M:%S.%f')
            check_out = datetime.strptime(checkin['check_out_time'], '%Y-%m-%d %H:%M:%S.%f')
            
            # Calculate hours worked
            time_diff = check_out - check_in
            hours_worked = time_diff.total_seconds() / 3600
            
            # Calculate cost
            daily_cost = hours_worked * hourly_rate
            
            billing_records.append({
                'date': checkin['date'],
                'check_in': check_in.strftime('%H:%M'),
                'check_out': check_out.strftime('%H:%M'),
                'hours_worked': round(hours_worked, 2),
                'hourly_rate': hourly_rate,
                'cost': round(daily_cost, 2),
                'status': checkin['status']
            })
            
            total_hours += hours_worked
            total_cost += daily_cost
    
    return {
        'records': billing_records,
        'total_hours': round(total_hours, 2),
        'total_cost': round(total_cost, 2),
        'hourly_rate': hourly_rate,
        'period_start': start_date,
        'period_end': end_date
    }
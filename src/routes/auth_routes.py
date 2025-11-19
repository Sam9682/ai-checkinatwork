"""Authentication routes"""
from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash
from ..database import get_db_connection

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        employee = conn.execute(
            'SELECT * FROM employees WHERE username = ? AND is_active = 1',
            (username,)
        ).fetchone()
        conn.close()
        
        if employee and check_password_hash(employee['password_hash'], password):
            session['employee_id'] = employee['id']
            session['username'] = employee['username']
            session['employee_name'] = f"{employee['first_name']} {employee['last_name']}"
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
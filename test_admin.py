#!/usr/bin/env python3
"""Test script to verify admin functionality"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import init_db, get_db_connection
from werkzeug.security import generate_password_hash
from datetime import date

def test_admin_setup():
    """Test admin functionality setup"""
    print("🧪 Testing admin functionality...")
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    conn = get_db_connection()
    
    # Check if admin user exists
    admin = conn.execute("SELECT * FROM employees WHERE username = 'admin'").fetchone()
    if admin:
        print(f"✅ Admin user exists: {admin['username']}")
        print(f"   Name: {admin['first_name']} {admin['last_name']}")
        print(f"   Email: {admin['email']}")
    else:
        print("❌ Admin user not found")
        return False
    
    # Check admin billing rate
    admin_rate = conn.execute('''
        SELECT hourly_rate FROM billing_rates 
        WHERE employee_id = ? AND is_active = 1
    ''', (admin['id'],)).fetchone()
    
    if admin_rate:
        print(f"✅ Admin billing rate: ${admin_rate['hourly_rate']}")
    else:
        print("❌ Admin billing rate not found")
    
    # Create a test user
    test_username = 'testuser'
    existing_test = conn.execute(
        'SELECT id FROM employees WHERE username = ?', (test_username,)
    ).fetchone()
    
    if not existing_test:
        password_hash = generate_password_hash('testpass')
        cursor = conn.execute('''
            INSERT INTO employees (employee_id, username, email, password_hash, first_name, last_name, department, position)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', ('EMP002', test_username, 'test@company.com', password_hash, 'Test', 'User', 'IT', 'Developer'))
        
        user_id = cursor.lastrowid
        
        # Create billing rate for test user
        conn.execute('''
            INSERT INTO billing_rates (employee_id, hourly_rate, effective_date)
            VALUES (?, ?, ?)
        ''', (user_id, 30.00, date.today()))
        
        conn.commit()
        print(f"✅ Test user created: {test_username}")
    else:
        print(f"✅ Test user already exists: {test_username}")
    
    # Count total users
    user_count = conn.execute('SELECT COUNT(*) as count FROM employees').fetchone()
    print(f"✅ Total users in system: {user_count['count']}")
    
    conn.close()
    print("🎉 Admin functionality test completed!")
    return True

if __name__ == '__main__':
    test_admin_setup()
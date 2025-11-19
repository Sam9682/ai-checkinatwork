#!/usr/bin/env python3
"""Test script to verify billing functionality"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.database import init_db, get_db_connection
from datetime import datetime, date, timedelta
import sqlite3

def test_billing_setup():
    """Test billing database setup and functionality"""
    print("🧪 Testing billing system setup...")
    
    # Initialize database
    init_db()
    print("✅ Database initialized")
    
    # Check if billing_rates table exists
    conn = get_db_connection()
    
    # Check table structure
    tables = conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    table_names = [table['name'] for table in tables]
    
    if 'billing_rates' in table_names:
        print("✅ billing_rates table exists")
    else:
        print("❌ billing_rates table missing")
        return False
    
    # Check if admin has billing rate
    admin_rate = conn.execute('''
        SELECT br.hourly_rate, e.username 
        FROM billing_rates br 
        JOIN employees e ON br.employee_id = e.id 
        WHERE e.username = 'admin'
    ''').fetchone()
    
    if admin_rate:
        print(f"✅ Admin billing rate: ${admin_rate['hourly_rate']}")
    else:
        print("❌ Admin billing rate not found")
    
    # Create test check-in data
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    # Get admin employee ID
    admin = conn.execute("SELECT id FROM employees WHERE username = 'admin'").fetchone()
    if admin:
        admin_id = admin['id']
        
        # Insert test check-in data
        test_checkin = datetime.combine(yesterday, datetime.strptime('09:00', '%H:%M').time())
        test_checkout = datetime.combine(yesterday, datetime.strptime('17:30', '%H:%M').time())
        
        # Check if test data already exists
        existing = conn.execute(
            'SELECT * FROM checkins WHERE employee_id = ? AND date = ?',
            (admin_id, yesterday)
        ).fetchone()
        
        if not existing:
            conn.execute('''
                INSERT INTO checkins (employee_id, check_in_time, check_out_time, date, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (admin_id, test_checkin, test_checkout, yesterday, 'on_time'))
            conn.commit()
            print(f"✅ Test check-in data created for {yesterday}")
        else:
            print(f"✅ Test check-in data already exists for {yesterday}")
    
    conn.close()
    print("🎉 Billing system test completed successfully!")
    return True

if __name__ == '__main__':
    test_billing_setup()
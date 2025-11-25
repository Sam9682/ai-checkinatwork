#!/usr/bin/env python3
"""Development server runner"""
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from src.app import create_app
    
    app = create_app()
    
    if __name__ == '__main__':
        print("🚀 Starting AI Check-in at Work Development Server")
        print("=" * 50)
        print("📍 URL: http://localhost:5000")
        print("👤 Default Login: admin / password")
        print("💰 Billing Report: http://localhost:5000/billing")
        print("=" * 50)
        
        app.run(host='0.0.0.0', port=5000, debug=True)
        
except ImportError as e:
    print(f"❌ Import Error: {e}")
    print("💡 Try installing dependencies: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    sys.exit(1)
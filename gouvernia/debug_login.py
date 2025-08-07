#!/usr/bin/env python3
"""
Debug script to test login functionality and database connectivity
"""

from app import app, db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

def debug_login():
    with app.app_context():
        print("=== DEBUGGING LOGIN ISSUES ===")
        
        # Check database connection
        try:
            db.session.execute(db.text('SELECT 1'))
            print("✅ Database connection: OK")
        except Exception as e:
            print(f"❌ Database connection error: {e}")
            return
        
        # Check if users exist
        users = User.query.all()
        print(f"\nFound {len(users)} users:")
        for user in users:
            print(f"  - {user.username} ({user.email}) - {user.role}")
        
        # Test password verification
        demo_user = User.query.filter_by(username='demo').first()
        if demo_user:
            print(f"\nTesting demo user:")
            print(f"  Username: {demo_user.username}")
            print(f"  Email: {demo_user.email}")
            print(f"  Password hash: {demo_user.password_hash}")
            
            # Test actual passwords
            test_passwords = ['demo123', 'demo', 'password', 'admin123']
            for pwd in test_passwords:
                result = check_password_hash(demo_user.password_hash, pwd)
                print(f"  Password '{pwd}': {'✅ VALID' if result else '❌ INVALID'}")
        else:
            print("❌ Demo user not found!")
            
        # Check admin user
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            print(f"\nTesting admin user:")
            result = check_password_hash(admin_user.password_hash, 'admin123')
            print(f"  admin/admin123: {'✅ VALID' if result else '❌ INVALID'}")

if __name__ == "__main__":
    debug_login()

#!/usr/bin/env python3
"""
Fix script to update password hashes for demo users
"""

from app import app, db
from models import User
from werkzeug.security import generate_password_hash

def fix_passwords():
    with app.app_context():
        # Fix demo user password
        demo_user = User.query.filter_by(username='demo').first()
        if demo_user:
            demo_user.set_password('demo123')
            db.session.commit()
            print('✅ Demo user password fixed: demo123')
        
        # Fix admin user password
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            admin_user.set_password('admin123')
            db.session.commit()
            print('✅ Admin user password fixed: admin123')
            
        # Fix budget_manager password
        budget_user = User.query.filter_by(username='budget_manager').first()
        if budget_user:
            budget_user.set_password('budget123')
            db.session.commit()
            print('✅ Budget manager password fixed: budget123')
            
        # Fix security_officer password
        security_user = User.query.filter_by(username='security_officer').first()
        if security_user:
            security_user.set_password('security123')
            db.session.commit()
            print('✅ Security officer password fixed: security123')
            
        print('All passwords updated successfully!')

if __name__ == "__main__":
    fix_passwords()

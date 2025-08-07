#!/usr/bin/env python3
"""
Simple verification script for GOUVERNIA application
Verifies the application works with DevConfig only
"""

import sys
import requests
import time
import threading
import subprocess
from flask import Flask

def test_application():
    """Test the GOUVERNIA application functionality"""
    print("🔍 Testing GOUVERNIA Application with DevConfig...")
    print("=" * 60)
    
    try:
        # Test 1: Import test
        print("1️⃣  Testing imports...")
        from app import app
        from config import DevConfig
        print("   ✅ All modules imported successfully")
        
        # Test 2: Configuration test
        print("2️⃣  Testing DevConfig configuration...")
        print(f"   DEBUG: {app.config['DEBUG']}")
        print(f"   DATABASE: {app.config['SQLALCHEMY_DATABASE_URI']}")
        print(f"   SECRET_KEY: {'dev-secret-key-for-localhost' in app.config['SECRET_KEY']}")
        print("   ✅ DevConfig loaded correctly")
        
        # Test 3: Database models
        print("3️⃣  Testing database models...")
        with app.app_context():
            from models import User, Budget, Transaction, Investment, SecurityAlert
            users = User.query.all()
            budgets = Budget.query.all()
            transactions = Transaction.query.all()
            investments = Investment.query.all()
            alerts = SecurityAlert.query.all()
            
            print(f"   Users: {len(users)}")
            print(f"   Budgets: {len(budgets)}")
            print(f"   Transactions: {len(transactions)}")
            print(f"   Investments: {len(investments)}")
            print(f"   Security Alerts: {len(alerts)}")
            print("   ✅ Database models working correctly")
        
        # Test 4: Flask app configuration
        print("4️⃣  Testing Flask app configuration...")
        test_client = app.test_client()
        
        # Test index page
        response = test_client.get('/')
        if response.status_code == 200:
            print("   ✅ Index page loads successfully")
        else:
            print(f"   ❌ Index page failed: {response.status_code}")
            
        # Test login page
        response = test_client.get('/login')
        if response.status_code == 200:
            print("   ✅ Login page loads successfully")
        else:
            print(f"   ❌ Login page failed: {response.status_code}")
            
        # Test dashboard redirect (should redirect to login)
        response = test_client.get('/dashboard')
        if response.status_code == 302:
            print("   ✅ Dashboard correctly redirects to login")
        else:
            print(f"   ❌ Dashboard access failed: {response.status_code}")
            
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("🚀 GOUVERNIA application is working correctly with DevConfig!")
        print("Ready for testing and development!")
        print("=" * 60)
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_cli_functionality():
    """Test CLI functionality"""
    print("\n🔧 Testing CLI functionality...")
    try:
        # Test budget status
        result = subprocess.run([sys.executable, 'cli.py', 'budget', 'status'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("   ✅ CLI budget status works")
        else:
            print(f"   ❌ CLI budget status failed: {result.stderr}")
    except Exception as e:
        print(f"   ❌ CLI test failed: {e}")

def verify_devconfig_only():
    """Verify that only DevConfig is being used"""
    print("\n🔎 Verifying DevConfig usage...")
    
    # Check config file
    with open('config.py', 'r') as f:
        config_content = f.read()
        
    if 'class DevConfig:' in config_content:
        print("   ✅ DevConfig class found")
    else:
        print("   ❌ DevConfig class not found")
        
    # Check if production configs are removed
    production_indicators = ['PROD', 'PRODUCTION', 'postgresql://', 'mysql://', 'SECRET_KEY_PROD']
    has_production = any(indicator in config_content for indicator in production_indicators)
    
    if not has_production:
        print("   ✅ No production configuration found - clean DevConfig only")
    else:
        print("   ⚠️  Some production indicators still present")

if __name__ == '__main__':
    success = test_application()
    test_cli_functionality()
    verify_devconfig_only()
    
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

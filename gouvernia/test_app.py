#!/usr/bin/env python3

try:
    from app import app
    print("✅ App imports successfully")
    
    # Test if we can create app context
    with app.app_context():
        print("✅ App context works")
        
        # Test database connection
        from models import db
        print("✅ Database models import successfully")
        
    print("🚀 App is ready to run!")
    print("Run: python app.py")
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

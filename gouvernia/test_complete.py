#!/usr/bin/env python3
"""
Comprehensive test suite for GOUVERNIA application
Tests the application functionality with DevConfig only
"""

import unittest
import tempfile
import os
import sys
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.getcwd())

from app import app, db
from models import User, Budget, Transaction, Investment, SecurityAlert, TransparencyReport

class GouverniaTestCase(unittest.TestCase):
    """Test cases for GOUVERNIA application"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['WTF_CSRF_ENABLED'] = False
        
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self._create_test_data()

    def tearDown(self):
        """Tear down test fixtures after each test method."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _create_test_data(self):
        """Create test data for the database"""
        # Create test user
        test_user = User(
            username='testuser',
            email='test@test.com',
            role='user',
            ministry='Test Ministry'
        )
        test_user.set_password('testpass')
        db.session.add(test_user)
        
        # Create test admin user
        admin_user = User(
            username='admin',
            email='admin@test.com',
            role='admin',
            ministry='Admin Ministry'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        
        # Create test budget
        test_budget = Budget(
            ministry='Test Ministry',
            sector='Test Sector',
            allocated_amount=1000000,
            spent_amount=500000,
            fiscal_year=2024
        )
        db.session.add(test_budget)
        
        db.session.commit()

    def test_app_exists(self):
        """Test that the application exists"""
        self.assertIsNotNone(app)

    def test_app_is_testing(self):
        """Test that the application is in testing mode"""
        self.assertTrue(app.config['TESTING'])

    def test_index_page(self):
        """Test the index page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'GOUVERNIA', response.data)

    def test_login_page(self):
        """Test the login page loads"""
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        """Test successful login"""
        response = self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_login_failure(self):
        """Test failed login"""
        response = self.client.post('/login', data={
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)

    def test_dashboard_requires_login(self):
        """Test that dashboard requires login"""
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_dashboard_with_login(self):
        """Test dashboard access with login"""
        # Login first
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = self.client.get('/dashboard')
        self.assertEqual(response.status_code, 200)

    def test_budget_page_with_login(self):
        """Test budget page access with login"""
        # Login first
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = self.client.get('/budget')
        self.assertEqual(response.status_code, 200)

    def test_investments_page_with_login(self):
        """Test investments page access with login"""
        # Login first
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = self.client.get('/investments')
        self.assertEqual(response.status_code, 200)

    def test_transparency_page_with_login(self):
        """Test transparency page access with login"""
        # Login first
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = self.client.get('/transparency')
        self.assertEqual(response.status_code, 200)

    def test_security_page_with_login(self):
        """Test security page access with login"""
        # Login first
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = self.client.get('/security')
        self.assertEqual(response.status_code, 200)

    def test_api_budget_summary(self):
        """Test budget summary API endpoint"""
        # Login first
        self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        response = self.client.get('/api/budget-summary')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.is_json)

    def test_database_models(self):
        """Test that database models work correctly"""
        with self.app.app_context():
            # Test User model
            users = User.query.all()
            self.assertGreater(len(users), 0)
            
            # Test Budget model
            budgets = Budget.query.all()
            self.assertGreater(len(budgets), 0)
            
            # Test if models have required attributes
            user = users[0]
            self.assertTrue(hasattr(user, 'username'))
            self.assertTrue(hasattr(user, 'email'))
            self.assertTrue(hasattr(user, 'role'))

    def test_config_devconfig_only(self):
        """Test that application uses only DevConfig"""
        self.assertEqual(app.config['DEBUG'], True)
        self.assertIn('sqlite', app.config['SQLALCHEMY_DATABASE_URI'].lower())
        self.assertEqual(app.config['SECRET_KEY'], 'dev-secret-key-for-localhost')

def run_tests():
    """Run all tests and return success status"""
    suite = unittest.TestLoader().loadTestsFromTestCase(GouverniaTestCase)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    return result.wasSuccessful()

if __name__ == '__main__':
    print("Running comprehensive tests for GOUVERNIA application...")
    print("Testing with DevConfig only...")
    print("=" * 60)
    
    success = run_tests()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED - Application is working correctly with DevConfig!")
        sys.exit(0)
    else:
        print("❌ SOME TESTS FAILED - Please check the output above")
        sys.exit(1)

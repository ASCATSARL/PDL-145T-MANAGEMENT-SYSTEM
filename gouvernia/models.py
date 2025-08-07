from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')
    ministry = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        return str(self.id)
    
    @property
    def is_authenticated(self):
        return True
    
    @property
    def is_active(self):
        return True
    
    @property
    def is_anonymous(self):
        return False

class Budget(db.Model):
    __tablename__ = 'budgets'
    
    id = db.Column(db.Integer, primary_key=True)
    ministry = db.Column(db.String(100), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    allocated_amount = db.Column(db.Float, nullable=False)
    spent_amount = db.Column(db.Float, default=0.0)
    fiscal_year = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    transactions = db.relationship('Transaction', backref='budget', lazy=True)

class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budgets.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    beneficiary = db.Column(db.String(200))
    reference_number = db.Column(db.String(100), unique=True)
    is_anomaly = db.Column(db.Boolean, default=False)
    anomaly_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Investment(db.Model):
    __tablename__ = 'investments'
    
    id = db.Column(db.Integer, primary_key=True)
    project_name = db.Column(db.String(200), nullable=False)
    sector = db.Column(db.String(100), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    total_budget = db.Column(db.Float, nullable=False)
    spent_amount = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.Date, nullable=False)
    expected_end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='planned')
    roi_score = db.Column(db.Float, default=0.0)
    efficiency_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SecurityAlert(db.Model):
    __tablename__ = 'security_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    alert_type = db.Column(db.String(100), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(100), nullable=False)
    territory = db.Column(db.String(100))
    description = db.Column(db.Text, nullable=False)
    risk_score = db.Column(db.Float, nullable=False)
    is_resolved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TransparencyReport(db.Model):
    __tablename__ = 'transparency_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(50), nullable=False)
    period_start = db.Column(db.Date, nullable=False)
    period_end = db.Column(db.Date, nullable=False)
    total_transactions = db.Column(db.Integer, default=0)
    total_amount = db.Column(db.Float, default=0.0)
    anomaly_count = db.Column(db.Integer, default=0)
    transparency_score = db.Column(db.Float, default=0.0)
    report_data = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
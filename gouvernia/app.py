from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import os
import logging
from datetime import datetime
from models import db, User, Budget, Transaction, Investment, SecurityAlert, TransparencyReport
from ai_modules import AIModuleFactory

# Initialize Flask app
app = Flask(__name__)
app.config.from_object("config.DevConfig")

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename=app.config['LOG_FILE'],
    level=getattr(logging, app.config['LOG_LEVEL']),
    format='%(asctime)s %(levelname)s: %(message)s'
)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Connexion réussie!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnexion réussie', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Dashboard statistics
    total_budget = db.session.query(db.func.sum(Budget.allocated_amount)).scalar() or 0
    total_spent = db.session.query(db.func.sum(Budget.spent_amount)).scalar() or 0
    total_investments = db.session.query(db.func.sum(Investment.total_budget)).scalar() or 0
    total_alerts = SecurityAlert.query.filter_by(is_resolved=False).count()
    
    # Recent transactions
    recent_transactions = Transaction.query.order_by(Transaction.created_at.desc()).limit(5).all()
    
    # Active investments
    active_investments = Investment.query.filter(
        Investment.status.in_(['planned', 'in_progress'])
    ).limit(5).all()
    
    return render_template('dashboard.html',
                         total_budget=total_budget,
                         total_spent=total_spent,
                         total_investments=total_investments,
                         total_alerts=total_alerts,
                         recent_transactions=recent_transactions,
                         active_investments=active_investments)

# Budget routes
@app.route('/budget')
@login_required
def budget():
    budgets = Budget.query.all()
    return render_template('budget.html', budgets=budgets)

@app.route('/budget/anomalies')
@login_required
def budget_anomalies():
    anomalies = Transaction.query.filter_by(is_anomaly=True).all()
    return render_template('budget_anomalies.html', anomalies=anomalies)

# Investment routes
@app.route('/investments')
@login_required
def investments():
    investments = Investment.query.all()
    
    # Pre-calculate chart data
    planned_count = len([i for i in investments if i.status == 'planned'])
    in_progress_count = len([i for i in investments if i.status == 'in_progress'])
    completed_count = len([i for i in investments if i.status == 'completed'])
    
    # Get unique sectors and their budget sums
    sectors = list(set([i.sector for i in investments]))
    sector_labels = sectors
    sector_values = [sum([i.total_budget for i in investments if i.sector == sector]) for sector in sectors]
    
    return render_template('investments.html', 
                         investments=investments,
                         planned_count=planned_count,
                         in_progress_count=in_progress_count,
                         completed_count=completed_count,
                         sector_labels=sector_labels,
                         sector_values=sector_values)

@app.route('/investments/optimize')
@login_required
def optimize_investments():
    # Investment optimization logic
    investments = Investment.query.filter_by(status='planned').all()
    return render_template('investments_optimize.html', investments=investments)

# Transparency routes
@app.route('/transparency')
@login_required
def transparency():
    reports = TransparencyReport.query.order_by(TransparencyReport.created_at.desc()).all()
    return render_template('transparency.html', reports=reports)

@app.route('/api/transparency-reports')
@login_required
def api_transparency_reports():
    """API endpoint for transparency reports with AI analysis"""
    try:
        transpa_fin = AIModuleFactory.get_transpa_fin()
        
        reports = TransparencyReport.query.order_by(TransparencyReport.created_at.desc()).all()
        transactions = Transaction.query.all()
        
        # AI transparency analysis
        transparency_score = transpa_fin.calculate_transparency_score(transactions, reports)
        
        return jsonify({
            'reports': [{
                'id': r.id,
                'report_type': r.report_type,
                'period_start': r.period_start.isoformat(),
                'period_end': r.period_end.isoformat(),
                'total_transactions': r.total_transactions,
                'total_amount': r.total_amount,
                'anomaly_count': r.anomaly_count,
                'transparency_score': r.transparency_score,
                'created_at': r.created_at.isoformat()
            } for r in reports],
            'ai_analysis': {
                'transparency_score': transparency_score,
                'recommendations': [
                    "Améliorer la documentation des transactions" if transparency_score < 0.7 else "Maintenir les standards actuels",
                    "Augmenter la fréquence des rapports" if len(reports) < 4 else "Fréquence des rapports adéquate"
                ],
                'data_quality': {
                    'total_transactions': len(transactions),
                    'total_reports': len(reports),
                    'score_level': 'EXCELLENT' if transparency_score > 0.9 else 'GOOD' if transparency_score > 0.7 else 'NEEDS_IMPROVEMENT'
                }
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Security routes
@app.route('/security')
@login_required
def security():
    alerts = SecurityAlert.query.filter_by(is_resolved=False).all()
    return render_template('security.html', alerts=alerts)

# API routes for data
@app.route('/api/budget-summary')
@login_required
def api_budget_summary():
    """API endpoint for budget summary with AI analysis"""
    try:
        # Initialize AI module
        budget_ai = AIModuleFactory.get_budget_guard()
        
        # Get all transactions for AI analysis
        transactions = Transaction.query.all()
        
        # Get budget summary
        summary = db.session.query(
            Budget.sector,
            db.func.sum(Budget.allocated_amount).label('allocated'),
            db.func.sum(Budget.spent_amount).label('spent')
        ).group_by(Budget.sector).all()
        
        # AI anomaly detection
        anomalies = []
        if len(transactions) > 5:
            budget_ai.train(transactions)
            anomalies = budget_ai.detect_anomalies(transactions)
        
        return jsonify({
            'budget_summary': [{
                'sector': s.sector,
                'allocated': float(s.allocated),
                'spent': float(s.spent)
            } for s in summary],
            'ai_analysis': {
                'total_transactions': len(transactions),
                'anomalies_detected': len(anomalies),
                'anomalies': anomalies[:5],
                'anomaly_rate': len(anomalies) / len(transactions) if transactions else 0
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/investment-summary')
@login_required
def api_investment_summary():
    """API endpoint for investment summary with AI optimization"""
    try:
        invest_ai = AIModuleFactory.get_invest_smart()
        
        investments = Investment.query.all()
        
        # Get basic summary
        summary = db.session.query(
            Investment.sector,
            db.func.count(Investment.id).label('count'),
            db.func.sum(Investment.total_budget).label('total')
        ).group_by(Investment.sector).all()
        
        # AI analysis
        recommendations = []
        if investments:
            recommendations = invest_ai.analyze_investments(investments)
        
        return jsonify({
            'investment_summary': [{
                'sector': s.sector,
                'count': s.count,
                'total': float(s.total)
            } for s in summary],
            'ai_recommendations': recommendations[:10],
            'portfolio_analysis': {
                'total_investments': len(investments),
                'avg_roi': sum(inv.roi_score for inv in investments) / len(investments) if investments else 0,
                'high_risk_count': sum(1 for inv in investments if inv.roi_score < 50)  # Using roi_score as risk indicator
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/security-summary')
@login_required
def api_security_summary():
    """API endpoint for security summary with AI threat analysis"""
    try:
        peace_net = AIModuleFactory.get_peace_net()
        
        alerts = SecurityAlert.query.filter_by(is_resolved=False).all()
        
        # Get basic summary
        summary = db.session.query(
            SecurityAlert.province,
            db.func.count(SecurityAlert.id).label('count'),
            db.func.avg(SecurityAlert.risk_score).label('avg_risk')
        ).filter_by(is_resolved=False).group_by(SecurityAlert.province).all()
        
        # AI threat analysis
        threat_analysis = []
        if alerts:
            threat_analysis = peace_net.analyze_security_alerts(alerts)
        
        return jsonify({
            'security_summary': [{
                'province': s.province,
                'count': s.count,
                'avg_risk': float(s.avg_risk) if s.avg_risk else 0
            } for s in summary],
            'ai_threat_analysis': threat_analysis[:10],
            'threat_overview': {
                'total_alerts': len(alerts),
                'critical_alerts': len([t for t in threat_analysis if t.get('severity_level') == 'CRITICAL']),
                'high_risk_alerts': len([t for t in threat_analysis if t.get('risk_score', 0) > 0.7])
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('error.html', error_code=404, error_message='Page non trouvée'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('error.html', error_code=500, error_message='Erreur interne du serveur'), 500

# CLI commands
@app.cli.command()
def init_db():
    """Initialize the database."""
    db.create_all()
    print('Database initialized successfully.')

@app.cli.command()
def seed_db():
    """Seed the database with sample data."""
    from datetime import datetime, timedelta
    
    # Create admin user
    admin = User(
        username='admin',
        email='admin@gouv.cd',
        role='admin',
        ministry='Présidence'
    )
    admin.set_password('admin123')
    db.session.add(admin)
    
    # Create demo user
    demo = User(
        username='demo',
        email='demo@gouv.cd',
        role='user',
        ministry='Finances'
    )
    demo.set_password('demo123')
    db.session.add(demo)
    
    # Sample budgets
    budgets = [
        Budget(ministry='Santé Publique', sector='Santé', allocated_amount=500000000, spent_amount=320000000, fiscal_year=2024),
        Budget(ministry='Éducation Nationale', sector='Éducation', allocated_amount=800000000, spent_amount=650000000, fiscal_year=2024),
        Budget(ministry='Infrastructures', sector='Infrastructures', allocated_amount=1200000000, spent_amount=890000000, fiscal_year=2024),
        Budget(ministry='Énergie', sector='Énergie', allocated_amount=900000000, spent_amount=600000000, fiscal_year=2024),
    ]
    
    for budget in budgets:
        db.session.add(budget)
    
    # Sample investments
    investments = [
        Investment(
            project_name='Construction Hôpital Kinshasa',
            sector='Santé',
            province='Kinshasa',
            total_budget=150000000,
            spent_amount=120000000,
            start_date=datetime.now().date() - timedelta(days=180),
            expected_end_date=datetime.now().date() + timedelta(days=180),
            status='in_progress',
            roi_score=85.5,
            efficiency_score=78.9
        ),
        Investment(
            project_name='Rénovation École Lubumbashi',
            sector='Éducation',
            province='Haut-Katanga',
            total_budget=75000000,
            spent_amount=75000000,
            start_date=datetime.now().date() - timedelta(days=365),
            expected_end_date=datetime.now().date() - timedelta(days=30),
            status='completed',
            roi_score=92.3,
            efficiency_score=95.1
        ),
    ]
    
    for investment in investments:
        db.session.add(investment)
    
    # Sample security alerts
    alerts = [
        SecurityAlert(
            alert_type='Tension Sociale',
            severity='medium',
            province='Kinshasa',
            territory='Limete',
            description='Tensions sociales liées au chômage des jeunes',
            risk_score=45.2
        ),
        SecurityAlert(
            alert_type='Instabilité Économique',
            severity='high',
            province='Haut-Katanga',
            territory='Lubumbashi',
            description='Fluctuations des prix du cuivre affectant l\'économie locale',
            risk_score=78.5
        ),
    ]
    
    for alert in alerts:
        db.session.add(alert)
    
    db.session.commit()
    print('Database seeded successfully.')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
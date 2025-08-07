import click
from flask.cli import with_appcontext
from models import db, User, Budget, Transaction, Investment, SecurityAlert, TransparencyReport
from app import app
from datetime import datetime, timedelta
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@click.group()
def cli():
    """Interface en ligne de commande pour le Système IA Gouvernementale."""
    pass

@cli.group()
def db_cmd():
    """Commandes de gestion de la base de données."""
    pass

@db_cmd.command()
@with_appcontext
def init():
    """Initialiser la base de données."""
    db.create_all()
    click.echo('Base de données initialisée avec succès.')

@db_cmd.command()
@with_appcontext
def reset():
    """Réinitialiser la base de données."""
    db.drop_all()
    db.create_all()
    click.echo('Base de données réinitialisée avec succès.')

@db_cmd.command()
@with_appcontext
def seed():
    """Insérer des données d\'exemple."""
    from datetime import datetime, timedelta
    
    # Clear existing data
    TransparencyReport.query.delete()
    SecurityAlert.query.delete()
    Transaction.query.delete()
    Investment.query.delete()
    Budget.query.delete()
    User.query.delete()
    
    # Create users
    users = [
        User(username='admin', email='admin@gouv.cd', role='admin', ministry='Présidence'),
        User(username='demo', email='demo@gouv.cd', role='user', ministry='Finances'),
        User(username='budget_manager', email='budget@gouv.cd', role='manager', ministry='Budget'),
        User(username='security_officer', email='security@gouv.cd', role='security', ministry='Intérieur'),
    ]
    
    for user in users:
        user.set_password('password123')
        db.session.add(user)
    
    # Create budgets
    budgets = [
        Budget(ministry='Santé Publique', sector='Santé', allocated_amount=500000000, spent_amount=320000000, fiscal_year=2024),
        Budget(ministry='Éducation Nationale', sector='Éducation', allocated_amount=800000000, spent_amount=650000000, fiscal_year=2024),
        Budget(ministry='Infrastructures', sector='Infrastructures', allocated_amount=1200000000, spent_amount=890000000, fiscal_year=2024),
        Budget(ministry='Énergie', sector='Énergie', allocated_amount=900000000, spent_amount=600000000, fiscal_year=2024),
        Budget(ministry='Agriculture', sector='Agriculture', allocated_amount=400000000, spent_amount=250000000, fiscal_year=2024),
        Budget(ministry='Justice', sector='Justice', allocated_amount=300000000, spent_amount=200000000, fiscal_year=2024),
    ]
    
    for budget in budgets:
        db.session.add(budget)
    
    db.session.flush()  # Get budget IDs
    
    # Create transactions
    transactions = [
        Transaction(budget_id=1, amount=50000000, description='Achat d\'équipement médical', transaction_type='equipment', beneficiary='Hôpital Mama Yemo'),
        Transaction(budget_id=1, amount=25000000, description='Formation du personnel médical', transaction_type='training', beneficiary='Ministère Santé'),
        Transaction(budget_id=2, amount=75000000, description='Construction école primaire', transaction_type='construction', beneficiary='Commune de Limete'),
        Transaction(budget_id=2, amount=15000000, description='Manuels scolaires', transaction_type='supplies', beneficiary='École primaire'),
        Transaction(budget_id=3, amount=100000000, description='Route Goma-Bukavu', transaction_type='infrastructure', beneficiary='Province Nord-Kivu'),
        Transaction(budget_id=4, amount=80000000, description='Centrale hydroélectrique', transaction_type='energy', beneficiary='REGIDESO'),
    ]
    
    for transaction in transactions:
        db.session.add(transaction)
    
    # Create investments
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
        Investment(
            project_name='Route Goma-Bukavu',
            sector='Infrastructures',
            province='Nord-Kivu',
            total_budget=300000000,
            spent_amount=200000000,
            start_date=datetime.now().date() - timedelta(days=90),
            expected_end_date=datetime.now().date() + timedelta(days=270),
            status='in_progress',
            roi_score=78.9,
            efficiency_score=82.3
        ),
        Investment(
            project_name='Centrale Inga III',
            sector='Énergie',
            province='Bas-Congo',
            total_budget=2000000000,
            spent_amount=500000000,
            start_date=datetime.now().date() - timedelta(days=365),
            expected_end_date=datetime.now().date() + timedelta(days=1095),
            status='planned',
            roi_score=95.0,
            efficiency_score=88.7
        ),
    ]
    
    for investment in investments:
        db.session.add(investment)
    
    # Create security alerts
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
        SecurityAlert(
            alert_type='Conflit Armé',
            severity='high',
            province='Nord-Kivu',
            territory='Goma',
            description='Activités de groupes armés dans la région',
            risk_score=85.7
        ),
        SecurityAlert(
            alert_type='Tension Ethnique',
            severity='medium',
            province='Kasaï-Central',
            territory='Kananga',
            description='Tensions intercommunautaires dans la région',
            risk_score=62.3
        ),
    ]
    
    for alert in alerts:
        db.session.add(alert)
    
    db.session.commit()
    click.echo('Données d\'exemple insérées avec succès.')

@cli.group()
def budget():
    """Commandes de gestion budgétaire."""
    pass

@budget.command()
def status():
    """Afficher le statut budgétaire global."""
    with app.app_context():
        budgets = Budget.query.all()
        
        click.echo("=== STATUT BUDGÉTAIRE ===")
        click.echo(f"{'Ministère':<25} {'Secteur':<15} {'Alloué':<15} {'Dépensé':<15} {'Taux':<10}")
        click.echo("-" * 80)
        
        total_allocated = 0
        total_spent = 0
        
        for budget in budgets:
            rate = (budget.spent_amount / budget.allocated_amount * 100) if budget.allocated_amount > 0 else 0
            click.echo(f"{budget.ministry:<25} {budget.sector:<15} {budget.allocated_amount:<15,.0f} "
                      f"{budget.spent_amount:<15,.0f} {rate:<10.1f}%")
            total_allocated += budget.allocated_amount
            total_spent += budget.spent_amount
        
        total_rate = (total_spent / total_allocated * 100) if total_allocated > 0 else 0
        click.echo("-" * 80)
        click.echo(f"{'TOTAL':<25} {'':<15} {total_allocated:<15,.0f} {total_spent:<15,.0f} {total_rate:<10.1f}%")

@budget.command()
def anomalies():
    """Détecter les anomalies dans les transactions."""
    with app.app_context():
        anomalies = Transaction.query.filter_by(is_anomaly=True).all()
        
        click.echo("=== TRANSACTIONS ANORMALES ===")
        if not anomalies:
            click.echo("Aucune anomalie détectée.")
            return
        
        click.echo(f"{'ID':<5} {'Montant':<12} {'Type':<15} {'Bénéficiaire':<20} {'Score':<10}")
        click.echo("-" * 70)
        
        for anomaly in anomalies:
            click.echo(f"{anomaly.id:<5} {anomaly.amount:<12,.0f} {anomaly.transaction_type:<15} "
                      f"{anomaly.beneficiary:<20} {anomaly.anomaly_score:<10.2f}")

@cli.group()
def investment():
    """Commandes de gestion des investissements."""
    pass

@investment.command()
def list():
    """Lister tous les projets d\'investissement."""
    with app.app_context():
        investments = Investment.query.all()
        
        click.echo("=== PROJETS D\'INVESTISSEMENT ===")
        click.echo(f"{'Nom':<30} {'Secteur':<15} {'Province':<15} {'Budget':<12} {'Statut':<12} {'ROI':<8}")
        click.echo("-" * 100)
        
        for inv in investments:
            click.echo(f"{inv.project_name:<30} {inv.sector:<15} {inv.province:<15} "
                      f"{inv.total_budget:<12,.0f} {inv.status:<12} {inv.roi_score:<8.1f}%")

@investment.command()
@click.option('--budget', default=1000000000, help='Budget total disponible')
def optimize(budget):
    """Optimiser le portefeuille d\'investissements."""
    with app.app_context():
        investments = Investment.query.filter_by(status='planned').all()
        
        click.echo(f"=== OPTIMISATION AVEC BUDGET: {budget:,.0f} FC ===")
        
        # Simple optimization based on ROI and efficiency
        optimized = sorted(investments, key=lambda x: (x.roi_score + x.efficiency_score) / 2, reverse=True)
        
        total_cost = 0
        selected_projects = []
        
        for inv in optimized:
            if total_cost + inv.total_budget <= budget:
                selected_projects.append(inv)
                total_cost += inv.total_budget
        
        click.echo(f"\nSélection optimale ({len(selected_projects)} projets):")
        click.echo(f"{'Nom':<30} {'Coût':<12} {'ROI':<8} {'Efficacité':<12}")
        click.echo("-" * 70)
        
        for inv in selected_projects:
            click.echo(f"{inv.project_name:<30} {inv.total_budget:<12,.0f} "
                      f"{inv.roi_score:<8.1f}% {inv.efficiency_score:<12.1f}%")
        
        click.echo(f"\nBudget total utilisé: {total_cost:,.0f} FC")
        click.echo(f"Budget restant: {budget - total_cost:,.0f} FC")

@cli.group()
def security():
    """Commandes de gestion de la sécurité."""
    pass

@security.command()
def alerts():
    """Afficher les alertes de sécurité actives."""
    with app.app_context():
        alerts = SecurityAlert.query.filter_by(is_resolved=False).all()
        
        click.echo("=== ALERTES DE SÉCURITÉ ACTIVES ===")
        if not alerts:
            click.echo("Aucune alerte active.")
            return
        
        click.echo(f"{'ID':<5} {'Type':<20} {'Sévérité':<10} {'Province':<15} {'Score':<10}")
        click.echo("-" * 70)
        
        for alert in alerts:
            click.echo(f"{alert.id:<5} {alert.alert_type:<20} {alert.severity:<10} "
                      f"{alert.province:<15} {alert.risk_score:<10.1f}")

@cli.group()
def user():
    """Commandes de gestion des utilisateurs."""
    pass

@user.command()
@click.option('--username', prompt=True)
@click.option('--email', prompt=True)
@click.option('--role', default='user')
@click.option('--ministry', prompt=True)
def create(username, email, role, ministry):
    """Créer un nouvel utilisateur."""
    with app.app_context():
        if User.query.filter_by(username=username).first():
            click.echo(f"L\'utilisateur {username} existe déjà.")
            return
        
        user = User(username=username, email=email, role=role, ministry=ministry)
        password = click.prompt('Mot de passe', hide_input=True)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        click.echo(f"Utilisateur {username} créé avec succès.")

@user.command()
def list():
    """Lister tous les utilisateurs."""
    with app.app_context():
        users = User.query.all()
        
        click.echo("=== UTILISATEURS ===")
        click.echo(f"{'ID':<5} {'Username':<15} {'Email':<25} {'Rôle':<10} {'Ministère':<20}")
        click.echo("-" * 80)
        
        for user in users:
            click.echo(f"{user.id:<5} {user.username:<15} {user.email:<25} "
                      f"{user.role:<10} {user.ministry:<20}")

@cli.group()
def report():
    """Commandes de rapport et statistiques."""
    pass

@report.command()
def dashboard():
    """Afficher le tableau de bord."""
    with app.app_context():
        total_budget = db.session.query(db.func.sum(Budget.allocated_amount)).scalar() or 0
        total_spent = db.session.query(db.func.sum(Budget.spent_amount)).scalar() or 0
        total_investments = db.session.query(db.func.sum(Investment.total_budget)).scalar() or 0
        total_alerts = SecurityAlert.query.filter_by(is_resolved=False).count()
        
        click.echo("=== TABLEAU DE BORD GOUVERNIA ===")
        click.echo(f"Budget total alloué: {total_budget:,.0f} FC")
        click.echo(f"Budget total dépensé: {total_spent:,.0f} FC")
        click.echo(f"Taux d\'exécution: {(total_spent/total_budget*100) if total_budget > 0 else 0:.1f}%")
        click.echo(f"Investissements totaux: {total_investments:,.0f} FC")
        click.echo(f"Alertes de sécurité actives: {total_alerts}")

@report.command()
@click.option('--format', type=click.Choice(['json', 'csv']), default='json')
@click.option('--output', default='data_export.json')
def export(format, output):
    """Exporter les données."""
    with app.app_context():
        import json
        
        data = {
            'budgets': [{
                'ministry': b.ministry,
                'sector': b.sector,
                'allocated_amount': b.allocated_amount,
                'spent_amount': b.spent_amount,
                'fiscal_year': b.fiscal_year
            } for b in Budget.query.all()],
            'investments': [{
                'project_name': i.project_name,
                'sector': i.sector,
                'province': i.province,
                'total_budget': i.total_budget,
                'status': i.status,
                'roi_score': i.roi_score
            } for i in Investment.query.all()],
            'security_alerts': [{
                'alert_type': sa.alert_type,
                'severity': sa.severity,
                'province': sa.province,
                'risk_score': sa.risk_score
            } for sa in SecurityAlert.query.all()]
        }
        
        if format == 'json':
            with open(output, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        
        click.echo(f"Données exportées vers {output}")

@cli.command()
def health():
    """Vérifier l\'état de santé du système."""
    try:
        with app.app_context():
            # Test database connection
            db.session.execute('SELECT 1')
            click.echo("✓ Connexion base de données: OK")
            
            # Test models
            models = [User, Budget, Transaction, Investment, SecurityAlert]
            for model in models:
                count = model.query.count()
                click.echo(f"✓ {model.__name__}: {count} enregistrements")
            
            click.echo("✓ Système en bon état de fonctionnement")
    except Exception as e:
        click.echo(f"✗ Erreur: {e}")

@cli.command()
def version():
    """Afficher les informations de version."""
    click.echo("Système IA Gouvernementale RDC (GOUVERNIA)")
    click.echo("Version: 1.0.0")
    click.echo("Build: PDL-145T")
    click.echo("Environnement: Development")

if __name__ == '__main__':
    cli()
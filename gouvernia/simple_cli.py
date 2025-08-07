#!/usr/bin/env python3
"""
Interface CLI simplifiée pour démonstration du Système IA Gouvernementale.
Ce fichier peut être exécuté indépendamment sans base de données.
"""

import click
from datetime import datetime
import json
import time

# Données d'exemple démonstratives
DEMO_DATA = {
    'budgets': [
        {
            'ministry': 'Santé Publique',
            'sector': 'Santé',
            'allocated_amount': 500000000,
            'spent_amount': 320000000,
            'fiscal_year': 2024,
            'execution_rate': 64.0
        },
        {
            'ministry': 'Éducation Nationale',
            'sector': 'Éducation',
            'allocated_amount': 800000000,
            'spent_amount': 650000000,
            'fiscal_year': 2024,
            'execution_rate': 81.3
        },
        {
            'ministry': 'Infrastructures',
            'sector': 'Infrastructures',
            'allocated_amount': 1200000000,
            'spent_amount': 890000000,
            'fiscal_year': 2024,
            'execution_rate': 74.2
        }
    ],
    'investments': [
        {
            'project_name': 'Construction Hôpital Kinshasa',
            'sector': 'Santé',
            'province': 'Kinshasa',
            'total_budget': 150000000,
            'status': 'in_progress',
            'roi_score': 85.5,
            'efficiency_score': 78.9
        },
        {
            'project_name': 'Rénovation École Lubumbashi',
            'sector': 'Éducation',
            'province': 'Haut-Katanga',
            'total_budget': 75000000,
            'status': 'completed',
            'roi_score': 92.3,
            'efficiency_score': 95.1
        },
        {
            'project_name': 'Route Goma-Bukavu',
            'sector': 'Infrastructures',
            'province': 'Nord-Kivu',
            'total_budget': 300000000,
            'status': 'in_progress',
            'roi_score': 78.9,
            'efficiency_score': 82.3
        }
    ],
    'security_alerts': [
        {
            'alert_type': 'Tension Sociale',
            'severity': 'medium',
            'province': 'Kinshasa',
            'risk_score': 45.2,
            'description': 'Tensions sociales liées au chômage des jeunes'
        },
        {
            'alert_type': 'Instabilité Économique',
            'severity': 'high',
            'province': 'Haut-Katanga',
            'risk_score': 78.5,
            'description': 'Fluctuations des prix du cuivre'
        }
    ]
}

@click.group()
def demo():
    """Démonstration du Système IA Gouvernementale RDC."""
    click.echo("🌍 Système IA Gouvernementale RDC (GOUVERNIA)")
    click.echo("Démonstration interactive des fonctionnalités")
    click.echo("=" * 50)

@demo.command()
def dashboard():
    """Afficher le tableau de bord démonstratif."""
    click.echo("📊 TABLEAU DE BORD GOUVERNIA")
    click.echo("=" * 50)
    
    total_budget = sum(b['allocated_amount'] for b in DEMO_DATA['budgets'])
    total_spent = sum(b['spent_amount'] for b in DEMO_DATA['budgets'])
    total_investments = sum(i['total_budget'] for i in DEMO_DATA['investments'])
    total_alerts = len(DEMO_DATA['security_alerts'])
    
    execution_rate = (total_spent / total_budget * 100) if total_budget > 0 else 0
    
    click.echo(f"💰 Budget total alloué: {total_budget:,.0f} FC")
    click.echo(f"💸 Budget total dépensé: {total_spent:,.0f} FC")
    click.echo(f"📈 Taux d'exécution: {execution_rate:.1f}%")
    click.echo(f"🏗️ Investissements totaux: {total_investments:,.0f} FC")
    click.echo(f"⚠️ Alertes de sécurité: {total_alerts}")
    click.echo(f"📅 Période: 2024")
    
    # Progress bar simulation
    click.echo("\n📊 Visualisation:")
    bar_length = 40
    filled_length = int(bar_length * execution_rate // 100)
    bar = '█' * filled_length + '░' * (bar_length - filled_length)
    click.echo(f"Exécution budgétaire: [{bar}] {execution_rate:.1f}%")

@demo.command()
def budget():
    """Afficher les informations budgétaires."""
    click.echo("💰 GESTION BUDGÉTAIRE")
    click.echo("=" * 50)
    
    click.echo(f"{'Ministère':<25} {'Secteur':<12} {'Alloué':<12} {'Dépensé':<12} {'Taux':<8}")
    click.echo("-" * 70)
    
    for budget in DEMO_DATA['budgets']:
        rate = budget['execution_rate']
        status = "✅" if rate >= 80 else "⚠️" if rate >= 50 else "❌"
        click.echo(f"{budget['ministry']:<25} {budget['sector']:<12} "
                  f"{budget['allocated_amount']:<12,.0f} {budget['spent_amount']:<12,.0f} "
                  f"{rate:<8.1f}% {status}")

@demo.command()
def investments():
    """Afficher les projets d'investissement."""
    click.echo("🏗️ PROJETS D'INVESTISSEMENT")
    click.echo("=" * 50)
    
    click.echo(f"{'Projet':<30} {'Secteur':<12} {'Province':<12} {'Budget':<12} {'Statut':<12} {'ROI':<8}")
    click.echo("-" * 90)
    
    for inv in DEMO_DATA['investments']:
        status_emoji = "🟢" if inv['status'] == 'completed' else "🟡" if inv['status'] == 'in_progress' else "🔴"
        click.echo(f"{inv['project_name']:<30} {inv['sector']:<12} {inv['province']:<12} "
                  f"{inv['total_budget']:<12,.0f} {status_emoji} {inv['status']:<10} "
                  f"{inv['roi_score']:<8.1f}%")

@demo.command()
def security():
    """Afficher les alertes de sécurité."""
    click.echo("⚠️ ALERTES DE SÉCURITÉ")
    click.echo("=" * 50)
    
    click.echo(f"{'Type':<20} {'Sévérité':<10} {'Province':<15} {'Score':<8} {'Status':<8}")
    click.echo("-" * 65)
    
    severity_emoji = {'low': '🟢', 'medium': '🟡', 'high': '🔴', 'critical': '🚨'}
    
    for alert in DEMO_DATA['security_alerts']:
        emoji = severity_emoji.get(alert['severity'], '⚪')
        click.echo(f"{alert['alert_type']:<20} {emoji} {alert['severity']:<8} "
                  f"{alert['province']:<15} {alert['risk_score']:<8.1f} "
                  f"{'Actif' if alert['risk_score'] > 50 else 'Surveillance'}")

@demo.command()
def transparency():
    """Afficher les rapports de transparence."""
    click.echo("📊 TRANSPARENCE FINANCIÈRE")
    click.echo("=" * 50)
    
    # Simulate transparency calculation
    total_transactions = 156
    total_amount = 2500000000
    anomaly_rate = 2.3
    transparency_score = 94.7
    
    click.echo(f"📈 Transactions analysées: {total_transactions}")
    click.echo(f"💰 Montant total: {total_amount:,.0f} FC")
    click.echo(f"🔍 Taux d'anomalies: {anomaly_rate}%")
    click.echo(f"✅ Score de transparence: {transparency_score}%")
    
    # Simulate blockchain verification
    click.echo("\n🔗 Vérification blockchain:")
    click.echo("✅ Toutes les transactions sont traçables")
    click.echo("✅ Signature cryptographique valide")
    click.echo("✅ Aucune altération détectée")

@demo.command()
def ai_analysis():
    """Afficher l'analyse IA des données."""
    click.echo("🤖 ANALYSE PAR INTELLIGENCE ARTIFICIELLE")
    click.echo("=" * 50)
    
    # Simulate AI analysis
    click.echo("📊 Analyse des anomalies budgétaires:")
    click.echo("• Détection de 3 transactions suspectes")
    click.echo("• Pattern de dépenses irrégulières identifié")
    click.echo("• Recommandation: audit approfondi")
    
    click.echo("\n📈 Prédictions d'investissement:")
    click.echo("• ROI projeté: 87.3%")
    click.echo("• Risque de dépassement: 15%")
    click.echo("• Recommandation: poursuivre le projet")
    
    click.echo("\n⚠️ Analyse de sécurité prédictive:")
    click.echo("• Risque de tension sociale: MODÉRÉ")
    click.echo("• Facteurs de risque: chômage jeunes")
    click.echo("• Recommandation: programmes d'emploi")

@demo.command()
@click.option('--export', is_flag=True, help='Exporter les données en JSON')
def export(export):
    """Exporter les données démonstratives."""
    if export:
        filename = f"gouvernia_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(DEMO_DATA, f, indent=2, ensure_ascii=False)
        click.echo(f"✅ Données exportées vers {filename}")
    else:
        click.echo(json.dumps(DEMO_DATA, indent=2, ensure_ascii=False))

@demo.command()
def simulate():
    """Simuler une journée d'opérations."""
    click.echo("🎮 SIMULATION JOURNALIÈRE")
    click.echo("=" * 50)
    
    operations = [
        "Analyse des transactions du jour...",
        "Détection d'anomalies budgétaires...",
        "Évaluation des investissements en cours...",
        "Scan des réseaux sociaux pour tensions...",
        "Génération des rapports de transparence...",
        "Mise à jour des scores de sécurité..."
    ]
    
    for op in operations:
        click.echo(f"⏳ {op}")
        time.sleep(1)
        click.echo("✅ Terminé")
    
    click.echo("\n🎉 Simulation complète!")
    click.echo("📊 Rapport quotidien généré")

if __name__ == '__main__':
    demo()
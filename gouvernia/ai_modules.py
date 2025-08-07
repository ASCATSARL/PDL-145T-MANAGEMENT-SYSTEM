"""
AI Modules Implementation for Gouvernia
BudgetGuard, InvestSmart, TranspaFin, PeaceNet
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
from datetime import datetime

class BudgetGuard:
    """AI module for budget anomaly detection"""
    
    def __init__(self):
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
        
    def prepare_features(self, transactions):
        """Prepare features for anomaly detection"""
        features = []
        for t in transactions:
            features.append([
                t.amount,
                len(t.description),
                t.transaction_type == 'expense',
                abs(t.amount) > 10000,
                t.created_at.weekday() >= 5,  # weekend
            ])
        return np.array(features)
    
    def train(self, transactions):
        """Train anomaly detection model"""
        if not transactions:
            return False
            
        features = self.prepare_features(transactions)
        features_scaled = self.scaler.fit_transform(features)
        
        self.model.fit(features_scaled)
        self.is_trained = True
        
        # Save model
        os.makedirs('models', exist_ok=True)
        joblib.dump(self.model, 'models/budgetguard_model.pkl')
        joblib.dump(self.scaler, 'models/budgetguard_scaler.pkl')
        
        return True
    
    def detect_anomalies(self, transactions):
        """Detect anomalies in transactions"""
        if not self.is_trained:
            return []
            
        features = self.prepare_features(transactions)
        features_scaled = self.scaler.transform(features)
        
        predictions = self.model.predict(features_scaled)
        anomaly_scores = self.model.score_samples(features_scaled)
        
        results = []
        for i, (pred, score) in enumerate(zip(predictions, anomaly_scores)):
            if pred == -1:  # anomaly
                results.append({
                    'transaction_id': transactions[i].id,
                    'anomaly_score': abs(score),
                    'confidence': abs(score),
                    'reason': self._get_anomaly_reason(transactions[i])
                })
        
        return results
    
    def _get_anomaly_reason(self, transaction):
        """Generate human-readable anomaly reason"""
        reasons = []
        
        if abs(transaction.amount) > 50000:
            reasons.append("Montant inhabituellement élevé")
        
        if len(transaction.description) < 5:
            reasons.append("Description trop vague")
            
        return "; ".join(reasons) if reasons else "Anomalie détectée"


class InvestSmart:
    """AI module for investment optimization"""
    
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False
        
    def prepare_features(self, investments):
        """Prepare features for investment analysis"""
        features = []
        for inv in investments:
            features.append([
                inv.amount,
                inv.expected_roi,
                inv.risk_level,
                inv.sector == 'infrastructure',
                inv.sector == 'technology',
                (datetime.now() - inv.created_at).days,
            ])
        return np.array(features)
    
    def analyze_investments(self, investments):
        """Analyze investment portfolio and provide recommendations"""
        if not investments:
            return []
            
        features = self.prepare_features(investments)
        
        # Simple scoring system
        recommendations = []
        for i, inv in enumerate(investments):
            score = self._calculate_investment_score(inv)
            recommendations.append({
                'investment_id': inv.id,
                'current_score': score,
                'recommendation': self._get_recommendation(score, inv),
                'expected_roi': inv.expected_roi * score,
                'risk_adjusted': inv.risk_level / score if score > 0 else 1
            })
        
        return sorted(recommendations, key=lambda x: x['current_score'], reverse=True)
    
    def _calculate_investment_score(self, investment):
        """Calculate investment score based on multiple factors"""
        score = 0.5  # base score
        
        # ROI factor
        score += min(investment.expected_roi / 100, 0.3)
        
        # Risk adjustment
        risk_penalty = investment.risk_level * 0.1
        score -= risk_penalty
        
        # Sector bonus for infrastructure
        if investment.sector == 'infrastructure':
            score += 0.2
            
        return max(0, min(1, score))
    
    def _get_recommendation(self, score, investment):
        """Generate recommendation based on score"""
        if score > 0.8:
            return "Investissement hautement recommandé"
        elif score > 0.6:
            return "Investissement recommandé avec surveillance"
        elif score > 0.4:
            return "Investissement modéré - évaluation continue"
        else:
            return "Investissement à risque - reconsidérer"


class TranspaFin:
    """AI module for transparency analysis"""
    
    def __init__(self):
        self.transparency_threshold = 0.7
        
    def calculate_transparency_score(self, transactions, reports):
        """Calculate transparency score for financial operations"""
        if not transactions:
            return 0.0
            
        # Calculate completeness score
        completeness = self._calculate_completeness(transactions)
        
        # Calculate documentation score
        documentation = self._calculate_documentation(transactions)
        
        # Calculate audit trail score
        audit_trail = self._calculate_audit_trail(transactions)
        
        # Calculate reporting frequency score
        reporting = self._calculate_reporting_frequency(reports)
        
        # Weighted average
        transparency_score = (
            completeness * 0.3 +
            documentation * 0.25 +
            audit_trail * 0.25 +
            reporting * 0.2
        )
        
        return min(1.0, max(0.0, transparency_score))
    
    def _calculate_completeness(self, transactions):
        """Calculate data completeness score"""
        complete_fields = 0
        total_fields = 0
        
        for t in transactions:
            fields = [t.amount, t.description, t.beneficiary, t.reference_number]
            complete_fields += sum(1 for f in fields if f is not None and str(f).strip())
            total_fields += len(fields)
        
        return complete_fields / total_fields if total_fields > 0 else 0.0
    
    def _calculate_documentation(self, transactions):
        """Calculate documentation quality score"""
        if not transactions:
            return 0.0
            
        good_descriptions = sum(1 for t in transactions 
                              if t.description and len(t.description.strip()) > 10)
        return good_descriptions / len(transactions)
    
    def _calculate_audit_trail(self, transactions):
        """Calculate audit trail completeness"""
        if not transactions:
            return 0.0
            
        has_reference = sum(1 for t in transactions 
                          if t.reference_number and len(str(t.reference_number)) > 5)
        return has_reference / len(transactions)
    
    def _calculate_reporting_frequency(self, reports):
        """Calculate reporting frequency score"""
        if not reports:
            return 0.0
            
        # Score based on recent reports
        recent_reports = sum(1 for r in reports 
                           if (datetime.now() - r.created_at).days < 30)
        return min(1.0, recent_reports / 4)  # Target 4 reports per month


class PeaceNet:
    """AI module for security threat detection"""
    
    def __init__(self):
        self.risk_threshold = 0.6
        
    def analyze_security_alerts(self, alerts):
        """Analyze security alerts and provide risk assessment"""
        if not alerts:
            return []
            
        risk_analysis = []
        for alert in alerts:
            risk_score = self._calculate_risk_score(alert)
            
            risk_analysis.append({
                'alert_id': alert.id,
                'risk_score': risk_score,
                'severity_level': self._get_severity_level(risk_score),
                'recommendations': self._get_recommendations(alert, risk_score),
                'priority': self._get_priority(risk_score)
            })
        
        return sorted(risk_analysis, key=lambda x: x['risk_score'], reverse=True)
    
    def _calculate_risk_score(self, alert):
        """Calculate risk score for security alert"""
        base_score = 0.5
        
        # Severity factor
        severity_map = {'low': 0.2, 'medium': 0.5, 'high': 0.8, 'critical': 1.0}
        severity_score = severity_map.get(alert.severity.lower(), 0.5)
        
        # Geographic factor
        high_risk_provinces = ['nord-kivu', 'sud-kivu', 'ituri']
        province_factor = 0.3 if alert.province.lower() in high_risk_provinces else 0.1
        
        # Alert type factor
        type_factors = {
            'conflict': 0.8,
            'corruption': 0.7,
            'fraud': 0.6,
            'security': 0.9
        }
        type_factor = type_factors.get(alert.alert_type.lower(), 0.4)
        
        risk_score = (severity_score + province_factor + type_factor) / 3
        return min(1.0, max(0.0, risk_score))
    
    def _get_severity_level(self, risk_score):
        """Convert risk score to severity level"""
        if risk_score >= 0.8:
            return "CRITICAL"
        elif risk_score >= 0.6:
            return "HIGH"
        elif risk_score >= 0.4:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _get_recommendations(self, alert, risk_score):
        """Generate recommendations based on risk assessment"""
        recommendations = []
        
        if risk_score > 0.7:
            recommendations.append("Action immédiate requise")
            recommendations.append("Notifier les autorités compétentes")
        
        if alert.severity.lower() == 'high':
            recommendations.append("Augmenter la surveillance")
            recommendations.append("Établir un plan d'urgence")
        
        if 'corruption' in alert.alert_type.lower():
            recommendations.append("Enquête approfondie recommandée")
            recommendations.append("Auditer les processus financiers")
        
        return recommendations
    
    def _get_priority(self, risk_score):
        """Get priority level based on risk score"""
        if risk_score > 0.8:
            return 1
        elif risk_score > 0.6:
            return 2
        elif risk_score > 0.4:
            return 3
        else:
            return 4


# Factory function to get AI modules
class AIModuleFactory:
    """Factory for AI modules"""
    
    @staticmethod
    def get_budget_guard():
        return BudgetGuard()
    
    @staticmethod
    def get_invest_smart():
        return InvestSmart()
    
    @staticmethod
    def get_transpa_fin():
        return TranspaFin()
    
    @staticmethod
    def get_peace_net():
        return PeaceNet()

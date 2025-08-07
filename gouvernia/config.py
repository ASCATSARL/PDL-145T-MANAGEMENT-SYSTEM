class DevConfig:
    # Flask configurations
    DEBUG = True
    TESTING = False
    
    # Database configuration - using SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///gouvernia.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Security configurations (minimal for local development)
    SECRET_KEY = 'dev-secret-key-for-localhost'
    WTF_CSRF_ENABLED = False  # Disabled for easier local development
    SESSION_COOKIE_HTTPONLY = False  # Simplified for localhost
    SESSION_COOKIE_SAMESITE = None  # Relaxed for local development
    
    # Application configurations
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file upload
    
    # Logging configuration
    LOG_FILE = 'logs/gouvernia.log'
    LOG_LEVEL = 'DEBUG'
    
    # AI/ML configurations
    ANOMALY_THRESHOLD = 0.7
    ROI_THRESHOLD = 0.6
    SECURITY_RISK_THRESHOLD = 0.5
    
    # RDC specific configurations
    MINISTRIES = {
        'PRESIDENCE': 'Présidence de la République',
        'FINANCES': 'Ministère des Finances',
        'SANTE': 'Ministère de la Santé Publique',
        'EDUCATION': 'Ministère de l\'Éducation Nationale',
        'INFRASTRUCTURES': 'Ministère des Infrastructures',
        'ENERGIE': 'Ministère de l\'Énergie',
        'JUSTICE': 'Ministère de la Justice',
        'INTERIEUR': 'Ministère de l\'Intérieur',
        'DEFENSE': 'Ministère de la Défense',
        'AFF_ETRANGERES': 'Ministère des Affaires Étrangères'
    }
    
    PROVINCES = [
        'Kinshasa', 'Kongo-Central', 'Kwango', 'Kwilu', 'Mai-Ndombe',
        'Equateur', 'Tshuapa', 'Mongala', 'Nord-Ubangi', 'Sud-Ubangi',
        'Tshopo', 'Tshopo', 'Bas-Uele', 'Haut-Uele', 'Ituri',
        'Nord-Kivu', 'Sud-Kivu', 'Maniema', 'Katanga', 'Kasaï-Occidental',
        'Kasaï-Oriental', 'Kasaï-Central', 'Lomami', 'Sankuru', 'Lulua'
    ]
    
    SECTORS = [
        'Santé', 'Éducation', 'Infrastructures', 'Énergie', 'Agriculture',
        'Industrie', 'Commerce', 'Justice', 'Sécurité', 'Transports',
        'Télécommunications', 'Environnement', 'Tourisme', 'Sports', 'Culture'
    ]

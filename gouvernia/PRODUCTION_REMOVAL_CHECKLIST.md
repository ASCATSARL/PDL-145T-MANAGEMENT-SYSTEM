# PRODUCTION AND TESTING ARTIFACTS REMOVAL CHECKLIST

## Overview

This checklist identifies all production-related code, configurations, and testing artifacts that must be removed or refactored from the GOUVERNIA system before any public release or deployment to prevent security vulnerabilities and data exposure.

---

## 🔐 AUTHENTICATION & CREDENTIALS (CRITICAL)

### Hard-coded Credentials

- [ ] **`config.py`** (Lines 7, 60-66, 68-76):
  - Remove default SECRET_KEY: `'dev-secret-key-change-in-production'`
  - Remove hardcoded database URIs in DevelopmentConfig and ProductionConfig
  - Replace with environment variable references only

- [ ] **`templates/login.html`** (Lines 39-40):
  - Remove demo credentials display: `"Demo credentials: admin / admin123"` and `"Demo credentials: demo / demo123"`

- [ ] **`app.py`** (Lines 324-341):
  - Remove hardcoded user creation in `seed_db()` function
  - Remove `admin.set_password('admin123')` and `demo.set_password('demo123')`

- [ ] **`cli.py`** (Lines 52-61):
  - Remove hardcoded user creation with `user.set_password('password123')`
  - Remove demo users: admin, demo, budget_manager, security_officer

### Debug Scripts with Credentials

- [ ] **`debug_login.py`** (ENTIRE FILE):
  - Contains hardcoded password testing: `['demo123', 'demo', 'password', 'admin123']`
  - Contains database connection debugging
  - **ACTION**: Delete entire file

- [ ] **`fix_passwords.py`** (ENTIRE FILE):
  - Contains hardcoded password fixes for all demo users
  - **ACTION**: Delete entire file

---

## 🗄️ DATABASE & DATA (CRITICAL)

### Database Files

- [ ] **`instance/iagov_dev.db`** (SQLite database file):
  - Contains production/development data with user accounts and passwords
  - **ACTION**: Delete file and add `instance/` to .gitignore

### Database Configuration

- [ ] **`config.py`** (Lines 8, 62, 66):
  - Remove development database URI: `'sqlite:///iagov_dev.db'`
  - Remove production database URI fallback: `'sqlite:///iagov_prod.db'`
  - **ACTION**: Use environment variables only

---

## 🤖 MACHINE LEARNING MODELS (HIGH PRIORITY)

### Trained Models

- [ ] **`models/budgetguard_model.pkl`** (137KB file):
  - Pre-trained anomaly detection model potentially containing sensitive patterns
  - **ACTION**: Delete and retrain on sanitized data

- [ ] **`models/budgetguard_scaler.pkl`** (719B file):
  - Scaler fitted on production data
  - **ACTION**: Delete and recreate

### Model Training Code

- [ ] **`ai_modules.py`** (Lines 48-50):
  - Remove automatic model saving to `models/` directory
  - Add proper model versioning and sanitization

---

## 📊 DEMO & TEST DATA (HIGH PRIORITY)

### Sample Data Generation

- [ ] **`app.py`** (Lines 318-409):
  - Remove entire `seed_db()` function containing:
    - Sample budgets for real RDC ministries
    - Sample investments with specific locations
    - Sample security alerts with real province names
  - **ACTION**: Replace with configurable test data generation

- [ ] **`cli.py`** (Lines 38-186):
  - Remove `seed()` command containing:
    - Real ministry names and budget allocations
    - Specific RDC provinces and territories
    - Realistic transaction amounts and descriptions
  - **ACTION**: Replace with sanitized demo data

- [ ] **`simple_cli.py`** (Lines 12-85):
  - Remove `DEMO_DATA` dictionary with:
    - Specific ministry budget information
    - Real province names and project details
    - Realistic security alert scenarios

### Configuration with Real Data

- [ ] **`config.py`** (Lines 33-58):
  - Remove real RDC ministry mapping (`MINISTRIES` dict)
  - Remove real RDC province list (`PROVINCES` list)
  - Remove sector-specific configurations
  - **ACTION**: Make configurable via environment/config files

---

## 🚨 LOGGING & DEBUG INFORMATION (HIGH PRIORITY)

### Log Files

- [ ] **`logs/iagov.log`** (60KB+ file):
  - Contains server access logs with IP addresses (masked as \***\*\*\*\***)
  - Contains Flask debugger PINs: `115-************`
  - Contains development server warnings
  - **ACTION**: Delete file and configure proper log rotation/sanitization

### Debug Configuration

- [ ] **`app.py`** (Line 13):
  - Remove hardcoded development config: `app.config.from_object(config['development'])`
  - **ACTION**: Make environment-dependent

- [ ] **`app.py`** (Line 414):
  - Remove debug mode in main: `app.run(debug=True)`
  - **ACTION**: Use environment variables for debug settings

---

## 🖥️ DEVELOPMENT ARTIFACTS (MEDIUM PRIORITY)

### Development Files

- [ ] **`test_app.py`** (ENTIRE FILE):
  - Simple development test script
  - **ACTION**: Move to proper test directory or delete

- [ ] **`__pycache__/`** (Directory):
  - Python cache files
  - **ACTION**: Add to .gitignore and delete

### VSCode Configuration

- [ ] **`.vscode/settings.json`**:
  - Development environment settings
  - **ACTION**: Add to .gitignore (optional, low risk)

---

## 🌐 SERVER & DEPLOYMENT CONFIG (MEDIUM PRIORITY)

### Flask Development Server

- [ ] **`app.py`** (Line 411-414):
  - Uses Flask development server: `app.run(debug=True)`
  - **ACTION**: Replace with WSGI server configuration

### Database Connection

- [x] **`models.py`** \u0026 **`config.py`**:
  - ~~PostgreSQL references to 'pdl_management' database~~ → **COMPLETED**: Migrated to SQLite
  - **ACTION**: ~~Ensure all database references use environment variables~~ → **COMPLETED**: Simplified to SQLite only

---

## 🛠️ INFRASTRUCTURE & CI/CD (NEEDS INVESTIGATION)

### Missing Files to Check

- [ ] **Docker configuration**: Search for Dockerfile, docker-compose.yml
- [ ] **CI/CD pipelines**: Search for .github/, .gitlab-ci.yml, .circleci/
- [ ] **Kubernetes manifests**: Search for _.yaml, _.yml with k8s resources
- [ ] **Environment files**: Search for .env, .env.local, .env.production
- [ ] **Deployment scripts**: Search for deploy.sh, setup.sh, install.sh

---

## 📋 RECOMMENDED ACTIONS

### Immediate (Critical Security)

1. **Delete all credential files**: `debug_login.py`, `fix_passwords.py`
2. **Remove hardcoded credentials** from all source files
3. **Delete database files**: `instance/iagov_dev.db`
4. **Delete log files**: `logs/iagov.log`
5. **Delete trained models**: `models/*.pkl`

### Configuration Refactoring

1. **Create environment template** file (`.env.example`)
2. **Implement proper secret management** (environment variables)
3. **Add comprehensive .gitignore** file
4. **Separate development/production configurations**

### Data Sanitization

1. **Replace real RDC data** with generic/fictional examples
2. **Remove specific geographic references**
3. **Replace real ministry names** with generic department names
4. **Sanitize all sample monetary amounts**

### Security Hardening

1. **Add security headers** configuration
2. **Implement proper session management**
3. **Add rate limiting** configuration
4. **Implement audit logging** (without sensitive data)

---

## 🔍 VALIDATION CHECKLIST

After cleanup, verify:

- [ ] No hardcoded passwords or secrets remain in any file
- [ ] No real government data or specific locations mentioned
- [ ] All database connections use environment variables
- [ ] No development-specific configurations in production code
- [ ] All sensitive files added to .gitignore
- [ ] No trained models with potentially sensitive data
- [ ] No log files with debug information or IP addresses
- [ ] Configuration supports multiple deployment environments

---

_Generated on: 2025-08-02_
_Repository: gouvernia - GOUVERNIA IA Gouvernementale RDC_

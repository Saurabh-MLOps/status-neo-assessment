# Social Support AI System - Setup Guide

## 🚀 Quick Setup Instructions

This guide provides step-by-step instructions to get the Social Support AI System up and running in minutes.

## 📋 Prerequisites

### System Requirements
- **Operating System**: Linux, macOS, or Windows (with WSL)
- **Python**: 3.8 or higher
- **RAM**: Minimum 8GB, Recommended 16GB+
- **Storage**: Minimum 4GB free space
- **Network**: Internet access for package installation

### Required Software
- **Python 3.8+**: [Download Python](https://www.python.org/downloads/)
- **Git**: [Download Git](https://git-scm.com/downloads)
- **PostgreSQL**: [Download PostgreSQL](https://www.postgresql.org/download/)
- **Docker** (Optional): [Download Docker](https://www.docker.com/products/docker-desktop/)

## 🔧 Installation Steps

### Step 1: Clone the Repository

```bash
# Clone the repository
git clone <your-repository-url>
cd "Status Neo - Assessment"

# Verify the structure
ls -la
```

**Expected Output:**
```
total 40
drwxr-xr-x  10 user  staff   320 Sep  2 06:30 .
drwxr-xr-x   3 user  staff    96 Sep  2 06:30 ..
-rw-r--r--   1 user  staff  1078 Sep  2 06:30 .env.example
-rw-r--r--   1 user  staff  1024 Sep  2 06:30 .gitignore
-rw-r--r--   1 user  staff  1078 Sep  2 06:30 LICENSE
-rw-r--r--   1 user  staff 12345 Sep  2 06:30 README.md
drwxr-xr-x   8 user  staff   256 Sep  2 06:30 app
drwxr-xr-x   4 user  staff   128 Sep  2 06:30 scripts
drwxr-xr-x   4 user  staff   128 Sep  2 06:30 docs
-rw-r--r--   1 user  staff  2048 Sep  2 06:30 requirements.txt
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Verify Python version
python --version
# Should show Python 3.8 or higher

# Upgrade pip
pip install --upgrade pip
```

### Step 3: Install Dependencies

```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import fastapi, streamlit, sqlalchemy; print('Dependencies installed successfully!')"
```

**Expected Output:**
```
Dependencies installed successfully!
```

### Step 4: Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit environment file
# On macOS/Linux:
nano .env

# On Windows:
# notepad .env
```

**Configure these key variables:**

```bash
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/social_support_db

# AI Model Configuration
MODEL_PATH=./models/eligibility_model.pkl
FEATURE_SCALER_PATH=./models/feature_scaler.pkl

# Security Configuration
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Logging Configuration
LOG_LEVEL=INFO
```

### Step 5: Set Up Database

#### Option A: Using Docker (Recommended)

```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Verify container is running
docker ps

# Expected Output:
# CONTAINER ID   IMAGE       COMMAND                  CREATED         STATUS         PORTS                    NAMES
# abc123def456   postgres    "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes   0.0.0.0:5432->5432/tcp   postgres
```

#### Option B: Local PostgreSQL

```bash
# On macOS (using Homebrew):
brew install postgresql
brew services start postgresql

# On Ubuntu/Debian:
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql

# On Windows:
# Download and install from https://www.postgresql.org/download/windows/
```

**Create Database and User:**

```bash
# Connect to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE social_support_db;
CREATE USER username WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE social_support_db TO username;
\q
```

### Step 6: Initialize Database

```bash
# Run database setup script
python scripts/setup_database.py

# Expected Output:
# Database setup completed successfully!
# Tables created: applicants, documents, extracted_data, decisions, audit_logs
```

### Step 7: Generate Test Data (Optional)

```bash
# Generate synthetic test data
python scripts/generate_synthetic_data.py

# Expected Output:
# Generated 100 synthetic applications
# Test data inserted successfully!
```

### Step 8: Start the Backend

```bash
# Start FastAPI server
python -m uvicorn app.api.main:app --reload --host 127.0.0.1 --port 8000

# Expected Output:
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:     Started reloader process [12345] using StatReload
# INFO:     Started server process [12346]
# INFO:     Waiting for application startup.
# INFO:     Application startup complete.
```

**Keep this terminal running!**

### Step 9: Start the Frontend

**Open a new terminal window:**

```bash
# Navigate to project directory
cd "Status Neo - Assessment"

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Start Streamlit app
streamlit run app/streamlit_app.py --server.port 8501

# Expected Output:
# You can now view your Streamlit app in your browser.
# Local URL: http://localhost:8501
# Network URL: http://192.168.1.100:8501
```

**Keep this terminal running too!**

### Step 10: Verify Installation

#### Backend Health Check

```bash
# Test backend connectivity
curl -s http://127.0.0.1:8000/health | python3 -m json.tool

# Expected Output:
{
    "status": "healthy",
    "timestamp": "2025-09-02T...",
    "version": "1.0.0",
    "services": {
        "database": "connected",
        "ai_models": "loaded",
        "document_processing": "ready"
    }
}
```

#### Frontend Access

1. **Open your browser**
2. **Navigate to**: http://localhost:8501
3. **Verify dashboard loads** with metrics and navigation

#### API Documentation

1. **Open your browser**
2. **Navigate to**: http://127.0.0.1:8000/docs
3. **Verify interactive API docs** are accessible

## 🧪 Testing the System

### Basic System Test

```bash
# Run comprehensive system test
python scripts/simple_test.py

# Expected Output:
# ✅ Configuration loaded successfully
# ✅ Database connection established
# ✅ AI agents initialized successfully
# ✅ All tests passed!
```

### API Endpoint Test

```bash
# Test API endpoints
python scripts/demo.py

# Expected Output:
# 🚀 Testing Social Support AI System...
# ✅ Health check passed
# ✅ Application submission test passed
# ✅ Status checking test passed
# ✅ Decision retrieval test passed
# 🎉 All tests completed successfully!
```

### Complete Workflow Test

```bash
# Test full AI workflow
python scripts/quick_demo.py

# Expected Output:
# 🤖 Multi-Agent AI System Demo
# ✅ Extraction Agent: Document processing successful
# ✅ Validation Agent: Data validation completed
# ✅ Eligibility Agent: ML decision generated
# ✅ Recommender Agent: Recommendations created
# 🎯 Workflow completed successfully!
```

## 🎯 First Application Submission

### 1. Access the Application

- **URL**: http://localhost:8501
- **Click**: "New Application" button

### 2. Fill Application Form

**Personal Information:**
- First Name: `Test`
- Last Name: `User`
- Email: `test@example.com`
- Phone: `1234567890`
- Address: `123 Test Street`
- City: `Mumbai`
- State: `Maharashtra`
- Postal Code: `400001`
- Country: `India`

**Financial Information:**
- Monthly Income: `75000`
- Employment Status: `Full-time`
- Employer Name: `Test Company`
- Employment Length: `24` months
- Family Size: `3`
- Dependents: `1`
- Date of Birth: `1990-01-01`

### 3. Upload Test Document

**Create a test document:**

```bash
# Create sample bank statement
echo "BANK STATEMENT - Test Account" > test_document.txt
echo "Account Holder: Test User" >> test_document.txt
echo "Monthly Income: 75000" >> test_document.txt
echo "Employment: Test Company" >> test_document.txt
```

**Upload the document** in the Streamlit form

### 4. Submit and Monitor

1. **Click**: "Submit Application"
2. **Watch**: Real-time processing status
3. **Review**: AI analysis results
4. **Check**: Decision and recommendations

## 🔍 Troubleshooting

### Common Issues and Solutions

#### 1. Database Connection Failed

**Error**: `connection to server at "localhost" (::1), port 5432 failed`

**Solutions:**
```bash
# Check PostgreSQL status
sudo systemctl status postgresql

# Start PostgreSQL service
sudo systemctl start postgresql

# Verify connection settings in .env
cat .env | grep DATABASE_URL

# Test connection manually
psql -h localhost -U username -d social_support_db
```

#### 2. Port Already in Use

**Error**: `[Errno 48] Address already in use`

**Solutions:**
```bash
# Find process using port
lsof -i :8000
lsof -i :8501

# Kill process
kill -9 <PID>

# Or use different ports
python -m uvicorn app.api.main:app --reload --host 127.0.0.1 --port 8001
streamlit run app/streamlit_app.py --server.port 8502
```

#### 3. Python Import Errors

**Error**: `ModuleNotFoundError: No module named 'app'`

**Solutions:**
```bash
# Ensure you're in the project directory
pwd
# Should show: /path/to/Status Neo - Assessment

# Set PYTHONPATH
export PYTHONPATH="/path/to/Status Neo - Assessment:$PYTHONPATH"

# Or run from project root
cd "Status Neo - Assessment"
python -m uvicorn app.api.main:app --reload
```

#### 4. Dependencies Installation Failed

**Error**: `ERROR: Could not find a version that satisfies the requirement`

**Solutions:**
```bash
# Upgrade pip
pip install --upgrade pip

# Install with specific Python version
python3.8 -m pip install -r requirements.txt

# Install packages individually
pip install fastapi uvicorn streamlit sqlalchemy psycopg2-binary
```

#### 5. Streamlit UI Not Loading

**Error**: `Port 8501 is already in use`

**Solutions:**
```bash
# Kill existing Streamlit processes
pkill -f streamlit

# Use different port
streamlit run app/streamlit_app.py --server.port 8502

# Check for background processes
ps aux | grep streamlit
```

### Debug Mode

Enable detailed logging for troubleshooting:

```bash
# Set debug environment variable
export LOG_LEVEL=DEBUG

# Restart services
# Backend and frontend will show detailed logs
```

### System Health Check

```bash
# Comprehensive health check
curl -s http://127.0.0.1:8000/health | python3 -m json.tool

# Check individual components
curl -s http://127.0.0.1:8000/test | python3 -m json.tool
```

## 🚀 Production Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f
```

### Environment-Specific Configuration

**Development:**
```bash
LOG_LEVEL=DEBUG
ENVIRONMENT=development
DEBUG_MODE=true
```

**Production:**
```bash
LOG_LEVEL=WARNING
ENVIRONMENT=production
DEBUG_MODE=false
SECURE_COOKIES=true
```

## 📊 Performance Monitoring

### System Metrics

```bash
# Monitor system resources
htop
# or
top

# Check disk usage
df -h

# Monitor memory usage
free -h
```

### Application Metrics

- **Response Times**: Monitor API endpoint performance
- **Throughput**: Track applications processed per hour
- **Error Rates**: Monitor system stability
- **Resource Usage**: CPU, memory, and disk utilization

## 🔒 Security Configuration

### Environment Security

```bash
# Generate secure keys
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Update .env with secure keys
SECRET_KEY=your-generated-secret-key
ENCRYPTION_KEY=your-generated-encryption-key
```

### Database Security

```bash
# Enable SSL connections
DATABASE_URL=postgresql://user:pass@localhost:5432/db?sslmode=require

# Set connection limits
DATABASE_POOL_SIZE=10
DATABASE_MAX_OVERFLOW=20
```

## 📚 Next Steps

### 1. Explore the System

- **Dashboard**: Navigate through different sections
- **API Documentation**: Test endpoints interactively
- **Sample Applications**: Submit test applications

### 2. Customize Configuration

- **Business Rules**: Adjust decision logic
- **AI Models**: Tune machine learning parameters
- **UI Elements**: Customize Streamlit interface

### 3. Integration

- **External APIs**: Connect to payment systems
- **Authentication**: Implement user management
- **Monitoring**: Set up logging and alerting

### 4. Scaling

- **Load Balancing**: Deploy multiple instances
- **Database Optimization**: Tune PostgreSQL settings
- **Caching**: Implement Redis for performance

## 🆘 Getting Help

### Documentation

- **README.md**: Main project overview
- **SOLUTION_SUMMARY.md**: Technical architecture details
- **PROJECT_STRUCTURE.md**: Code organization guide
- **DEMO_SCRIPT.md**: Complete demonstration guide

### Support Resources

- **GitHub Issues**: Report bugs and request features
- **API Documentation**: Interactive endpoint testing
- **System Logs**: Detailed error information
- **Health Checks**: System status monitoring

### Community

- **Discussions**: Join community forums
- **Contributions**: Submit pull requests
- **Feedback**: Share your experience

---

**🎉 Congratulations! You've successfully set up the Social Support AI System.**

The system is now ready to process applications, analyze documents, and provide intelligent decision-making for social support evaluations. Start exploring the features and customize the system for your specific needs. 
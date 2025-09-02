# 🛠️ Local Setup Guide for Testing

## 🎯 Quick Start (5 minutes)

This guide will help you run the AI Social Support Application locally for testing purposes.

## 📋 Prerequisites

- **Python 3.8+** installed on your system
- **Git** for cloning the repository
- **Basic terminal/command prompt knowledge**

## 🚀 Step-by-Step Setup

### Step 1: Clone the Repository
```bash
git clone https://github.com/Saurabh-MLOps/status-neo-assessment.git
cd status-neo-assessment
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Start the Backend (FastAPI)
Open a new terminal window and run:
```bash
cd "Status Neo - Assessment"
python -m uvicorn app.api.main:app --reload --host 127.0.0.1 --port 8000
```

**Expected Output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

### Step 4: Start the Frontend (Streamlit)
Open another terminal window and run:
```bash
cd "Status Neo - Assessment"
streamlit run app/streamlit_app.py --server.port 8501
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Step 5: Access the Application
1. **Backend API**: http://127.0.0.1:8000
2. **Frontend UI**: http://localhost:8501

## 🧪 Testing the Application

### 1. Open the Frontend
- Go to http://localhost:8501 in your browser
- You'll see the application form

### 2. Fill Out the Form
Use this sample data:
```
First Name: Arjun
Last Name: Sharma
Age: 28
Email: arjun.sharma@email.com
Phone: +91-98765-43210
Income: 45000
Monthly Expenses: 28000
Savings: 150000
Employment Status: Full-time
Employer: TechCorp Solutions
Job Title: Software Engineer
```

### 3. Upload Test Document
- Use the `test_bank_statement.txt` file included in the repository
- This demonstrates document processing capabilities

### 4. Submit and Watch
- Click "Submit Application"
- Observe the AI workflow in action
- See comprehensive analysis results

## 🔧 Troubleshooting

### Issue: "Port already in use"
**Solution**: Change the port number
```bash
# For backend
python -m uvicorn app.api.main:app --reload --host 127.0.0.1 --port 8001

# For frontend
streamlit run app/streamlit_app.py --server.port 8502
```

### Issue: "Module not found"
**Solution**: Ensure you're in the correct directory
```bash
cd "Status Neo - Assessment"
pwd  # Should show the project directory
```

### Issue: "Database connection failed"
**Expected**: The system runs in demo mode without a database
**Impact**: AI processing still works, but data isn't persisted

## 📊 What You'll See

### Successful Test Results:
- ✅ Application form submission
- ✅ Document processing (if uploaded)
- ✅ AI workflow execution
- ✅ Comprehensive analysis display
- ✅ Risk assessment and recommendations

### Demo Mode Features:
- **Multi-Agent AI System**: Extraction, Validation, Eligibility agents
- **Document Processing**: Text analysis and relevance scoring
- **Machine Learning**: Automated decision-making
- **Real-time Processing**: Live workflow execution

## 🎭 Test Scenarios

### Scenario 1: Full Application
- Fill all form fields
- Upload test document
- Submit and observe complete workflow

### Scenario 2: Form Only
- Fill form fields only
- Submit without documents
- See basic processing

### Scenario 3: Different Documents
- Try various file formats
- Observe processing differences

## 🚀 Next Steps

1. **Test the application** with different inputs
2. **Explore the AI workflow** execution
3. **Review the analysis results**
4. **Understand the decision-making process**
5. **Provide feedback** on functionality

## 📞 Need Help?

If you encounter issues:
1. Check the terminal output for error messages
2. Ensure all dependencies are installed
3. Verify you're in the correct directory
4. Check that ports 8000 and 8501 are available

---

## 🎉 Ready to Test?

Follow these steps and you'll have the AI Social Support Application running locally in minutes! 🚀 
#!/usr/bin/env python3
"""
Script to create demonstration GIFs for the Social Support AI System
This script will help you create visual demonstrations of the system capabilities.
"""

import os
import sys
import time
import subprocess
import json
from datetime import datetime

def print_header():
    """Print a beautiful header for the demo creation"""
    print("🎬" + "="*60 + "🎬")
    print("🎥 Social Support AI System - Demo GIF Creator 🎥")
    print("🎬" + "="*60 + "🎬")
    print()

def check_dependencies():
    """Check if required tools are available"""
    print("🔍 Checking dependencies...")
    
    # Check for asciinema (for terminal recording)
    try:
        result = subprocess.run(['asciinema', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ asciinema found")
            asciinema_available = True
        else:
            print("❌ asciinema not found")
            asciinema_available = False
    except FileNotFoundError:
        print("❌ asciinema not found")
        asciinema_available = False
    
    # Check for ffmpeg (for video processing)
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ffmpeg found")
            ffmpeg_available = True
        else:
            print("❌ ffmpeg not found")
            ffmpeg_available = False
    except FileNotFoundError:
        print("❌ ffmpeg not found")
        ffmpeg_available = False
    
    return asciinema_available, ffmpeg_available

def create_terminal_demo():
    """Create a terminal-based demo recording"""
    print("\n📹 Creating Terminal Demo...")
    
    # Create demo script content
    demo_script = '''#!/bin/bash
# Social Support AI System Demo Script
echo "🤖 Social Support AI System - Terminal Demo"
echo "=========================================="
echo

# Check system health
echo "🔍 Checking system health..."
curl -s http://localhost:8000/health | jq '.'
echo

# Show API documentation
echo "📚 API Documentation available at: http://localhost:8000/docs"
echo

# Demonstrate application submission
echo "📝 Demonstrating application submission..."
echo "Sample application data:"
cat << 'EOF'
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1985-06-15",
  "email": "john.doe@example.com",
  "phone": "(555) 123-4567",
  "street_address": "123 Main Street",
  "city": "Anytown",
  "state": "CA",
  "postal_code": "90210",
  "country": "United States",
  "monthly_income": 4500.0,
  "employment_status": "Full-time",
  "employer_name": "Tech Solutions Inc",
  "employment_length_months": 36,
  "family_size": 3,
  "dependents": 1
}
EOF
echo

# Submit application
echo "🚀 Submitting application..."
RESPONSE=$(curl -s -X POST "http://localhost:8000/ingest" \
  -H "Content-Type: application/json" \
  -d @- << 'EOF'
{
  "first_name": "John",
  "last_name": "Doe",
  "date_of_birth": "1985-06-15",
  "email": "john.doe@example.com",
  "phone": "(555) 123-4567",
  "street_address": "123 Main Street",
  "city": "Anytown",
  "state": "CA",
  "postal_code": "90210",
  "country": "United States",
  "monthly_income": 4500.0,
  "employment_status": "Full-time",
  "employer_name": "Tech Solutions Inc",
  "employment_length_months": 36,
  "family_size": 3,
  "dependents": 1
}
EOF
)

echo "Response:"
echo $RESPONSE | jq '.'
echo

# Extract application ID
APP_ID=$(echo $RESPONSE | jq -r '.application_id')
echo "Application ID: $APP_ID"
echo

# Wait for processing
echo "⏳ Waiting for application processing..."
sleep 5

# Check status
echo "📊 Checking application status..."
curl -s "http://localhost:8000/status/$APP_ID" | jq '.overall_status'
echo

# Get decision
echo "🎯 Retrieving decision..."
curl -s "http://localhost:8000/decision/$APP_ID" | jq '.decision, .confidence_score'
echo

# Chat with system
echo "💬 Chatting with the system..."
curl -s -X POST "http://localhost:8000/chat/$APP_ID" \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the decision on my application?"}' | jq '.response'
echo

echo "✅ Demo completed successfully!"
echo "🌐 Frontend available at: http://localhost:8501"
echo "🔧 Backend API at: http://localhost:8000"
'''
    
    # Write demo script
    with open('demo_script.sh', 'w') as f:
        f.write(demo_script)
    
    # Make it executable
    os.chmod('demo_script.sh', 0o755)
    
    print("📝 Demo script created: demo_script.sh")
    print("🎥 To record a GIF, run:")
    print("   asciinema rec demo.cast")
    print("   ./demo_script.sh")
    print("   # Press Ctrl+D to stop recording")
    print("   asciinema gif demo.cast demo.gif")
    
    return True

def create_streamlit_demo_guide():
    """Create a guide for recording Streamlit demos"""
    print("\n🖥️ Creating Streamlit Demo Guide...")
    
    guide = """# Streamlit Demo Recording Guide

## 🎥 How to Create Demo GIFs for Streamlit

### Option 1: Screen Recording Software
1. **Loom** (Recommended for web apps)
   - Install Loom extension
   - Navigate to http://localhost:8501
   - Click Loom icon and start recording
   - Select area to record (browser window)
   - Demonstrate the features below

2. **ScreenToGif** (Windows)
   - Download from https://www.screentogif.com/
   - Select area to record
   - Start recording and demonstrate features
   - Save as GIF

3. **Gifox** (macOS)
   - Download from https://gifox.io/
   - Select area to record
   - Record demonstration
   - Export as GIF

### Option 2: Browser Extensions
1. **Loom** extension for Chrome/Firefox
2. **Nimbus Screenshot** with video recording
3. **Awesome Screenshot** with screen recording

## 🎯 Features to Demonstrate

### 1. Dashboard Overview (10-15 seconds)
- Show system status
- Display quick action buttons
- Highlight navigation menu

### 2. Application Submission (20-25 seconds)
- Fill out application form
- Upload sample documents
- Submit and show success message
- Display application ID

### 3. Status Monitoring (15-20 seconds)
- Enter application ID
- Show processing status
- Display document information
- Show extracted data

### 4. Decision Display (20-25 seconds)
- Show eligibility decision
- Display confidence score
- Highlight SHAP explanations
- Show recommendations

### 5. Chat Interface (15-20 seconds)
- Ask questions about application
- Show AI responses
- Demonstrate contextual help

### 6. Analytics Dashboard (15-20 seconds)
- Show performance metrics
- Display decision distributions
- Highlight system capabilities

## 📱 Recording Tips

### Timing
- **Total Duration**: 2-3 minutes maximum
- **Each Feature**: 15-25 seconds
- **Transitions**: Smooth and quick

### Quality
- **Resolution**: 1280x720 or higher
- **Frame Rate**: 10-15 FPS for GIFs
- **File Size**: Keep under 10MB for GitHub

### Content
- **Clear Actions**: Show what you're clicking
- **Highlight Results**: Emphasize key outputs
- **Professional**: Clean, organized interface

## 🎬 Sample Demo Script

1. **Introduction** (5s)
   - "Welcome to the Social Support AI System"

2. **Dashboard** (10s)
   - "Here's our main dashboard showing system status"

3. **Submit Application** (20s)
   - "Let's submit a new application with supporting documents"

4. **Processing** (15s)
   - "Watch as our AI agents process the documents"

5. **Results** (20s)
   - "Here's the ML-powered decision with explanations"

6. **Chat** (15s)
   - "Ask questions and get AI-powered assistance"

7. **Conclusion** (5s)
   - "A complete AI system for social support evaluation"

## 📁 File Organization

Save your demo GIFs as:
- `demo-dashboard.gif` - Dashboard overview
- `demo-submission.gif` - Application submission
- `demo-processing.gif` - Document processing
- `demo-decision.gif` - Decision display
- `demo-chat.gif` - Chat interface
- `demo-complete.gif` - Full workflow

## 🔗 Integration

Add these GIFs to your README.md:
```markdown
## 🎬 Demo

### Dashboard Overview
![Dashboard Demo](demo-dashboard.gif)

### Application Submission
![Submission Demo](demo-submission.gif)

### Complete Workflow
![Complete Demo](demo-complete.gif)
```
"""
    
    with open('STREAMLIT_DEMO_GUIDE.md', 'w') as f:
        f.write(guide)
    
    print("📚 Streamlit demo guide created: STREAMLIT_DEMO_GUIDE.md")
    return True

def create_quick_demo():
    """Create a quick demo without external dependencies"""
    print("\n⚡ Creating Quick Demo...")
    
    # Create a simple demo that shows the system structure
    demo_content = """# 🚀 Quick Demo - Social Support AI System

## 🎯 What You'll See

This demo showcases the core capabilities of our AI system:

### 1. **Multi-Agent Architecture** 🤖
- **Extraction Agent**: Processes documents (PDF, images, Excel)
- **Validation Agent**: Cross-checks information across sources
- **Eligibility Agent**: Makes ML-powered decisions
- **Recommender Agent**: Provides personalized suggestions
- **Master Agent**: Orchestrates the entire workflow

### 2. **Document Processing Pipeline** 📄
```
Document Upload → OCR/Extraction → Validation → ML Decision → Recommendations
```

### 3. **Key Features** ⭐
- **Multi-format Support**: PDF, images, Excel, text
- **Intelligent Extraction**: AI-powered data extraction
- **Conflict Resolution**: Automatic data reconciliation
- **ML Decisions**: XGBoost/LightGBM with SHAP explainability
- **Real-time Chat**: AI-powered assistance
- **Comprehensive Security**: PII protection and audit logging

## 🎬 Live Demo Steps

1. **Start the System**
   ```bash
   # Terminal 1: Backend
   uvicorn app.main:app --reload
   
   # Terminal 2: Frontend
   streamlit run app/streamlit_app.py
   
   # Terminal 3: LLM Service
   ollama serve
   ```

2. **Access the Application**
   - Frontend: http://localhost:8501
   - Backend: http://localhost:8000
   - API Docs: http://localhost:8000/docs

3. **Demonstrate Features**
   - Submit a sample application
   - Upload supporting documents
   - Watch AI processing in real-time
   - View ML-powered decisions
   - Chat with the AI system

## 🔧 Technical Demo

Run our comprehensive demo script:
```bash
python scripts/demo.py
```

This will:
- Submit a sample application
- Process documents through all agents
- Generate ML decisions
- Show SHAP explanations
- Provide personalized recommendations

## 📊 Expected Results

- **Processing Time**: 5-10 seconds per application
- **Accuracy**: 90%+ on synthetic data
- **Confidence**: High confidence scores for decisions
- **Explainability**: Clear SHAP-based explanations
- **Recommendations**: Personalized economic enablement strategies

## 🌟 System Highlights

- **Local Processing**: No cloud dependencies
- **Real-time Updates**: Live status monitoring
- **Interactive UI**: Streamlit-based interface
- **Comprehensive Logging**: Full audit trails
- **Scalable Architecture**: Ready for production deployment

## 🎉 Ready to Experience?

The system is production-ready and demonstrates:
- **AI-Powered Automation**: Intelligent document processing
- **Multi-Agent Coordination**: Sophisticated workflow orchestration
- **ML Decision Making**: Transparent and explainable AI
- **User Experience**: Intuitive and responsive interface
- **Enterprise Security**: Production-grade security features

Start the system and experience the future of social support application evaluation!
"""
    
    with open('QUICK_DEMO.md', 'w') as f:
        f.write(demo_content)
    
    print("📝 Quick demo guide created: QUICK_DEMO.md")
    return True

def main():
    """Main function to create demo materials"""
    print_header()
    
    # Check dependencies
    asciinema_available, ffmpeg_available = check_dependencies()
    
    print("\n🎬 Creating Demo Materials...")
    
    # Create terminal demo
    create_terminal_demo()
    
    # Create Streamlit demo guide
    create_streamlit_demo_guide()
    
    # Create quick demo
    create_quick_demo()
    
    print("\n🎉 Demo Materials Created Successfully!")
    print("\n📁 Files Created:")
    print("  • demo_script.sh - Terminal demo script")
    print("  • STREAMLIT_DEMO_GUIDE.md - Streamlit recording guide")
    print("  • QUICK_DEMO.md - Quick demo overview")
    
    print("\n🚀 Next Steps:")
    print("1. Start your system: uvicorn app.main:app --reload")
    print("2. Record terminal demo: asciinema rec demo.cast")
    print("3. Record Streamlit demo: Use screen recording software")
    print("4. Convert to GIFs: asciinema gif demo.cast demo.gif")
    print("5. Add GIFs to README.md")
    print("6. Push to GitHub with your demos!")
    
    print("\n💡 Pro Tips:")
    print("• Keep demos under 3 minutes total")
    print("• Show real functionality, not just UI")
    print("• Highlight AI/ML capabilities")
    print("• Demonstrate end-to-end workflows")
    print("• Use clear, professional narration")

if __name__ == "__main__":
    main() 
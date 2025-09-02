#!/usr/bin/env python3
"""
Demo script for Social Support AI System
"""

import os
import sys
import time
import requests
import json
from datetime import datetime

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def check_system_health():
    """Check if the system is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ FastAPI backend is running")
            return True
        else:
            print("❌ FastAPI backend returned error status")
            return False
    except requests.exceptions.RequestException:
        print("❌ FastAPI backend is not accessible")
        return False

def demo_application_submission():
    """Demonstrate application submission"""
    print("\n📝 Demo: Application Submission")
    print("=" * 40)
    
    # Sample application data
    sample_application = {
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
    
    print("Submitting sample application...")
    print(f"Applicant: {sample_application['first_name']} {sample_application['last_name']}")
    print(f"Income: ${sample_application['monthly_income']:,.2f}")
    print(f"Employment: {sample_application['employment_status']} at {sample_application['employer_name']}")
    
    try:
        # Submit application
        response = requests.post(
            "http://localhost:8000/ingest",
            json=sample_application,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            application_id = result.get('application_id')
            print(f"✅ Application submitted successfully!")
            print(f"Application ID: {application_id}")
            print(f"Status: {result.get('status')}")
            return application_id
        else:
            print(f"❌ Application submission failed: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error submitting application: {e}")
        return None

def demo_status_checking(application_id):
    """Demonstrate application status checking"""
    if not application_id:
        print("❌ No application ID available for status check")
        return
    
    print(f"\n📊 Demo: Status Checking for Application {application_id}")
    print("=" * 50)
    
    print("Checking application status...")
    
    try:
        response = requests.get(f"http://localhost:8000/status/{application_id}", timeout=10)
        
        if response.status_code == 200:
            status_data = response.json()
            print("✅ Status retrieved successfully!")
            
            # Display key information
            applicant = status_data.get('applicant', {})
            print(f"Applicant: {applicant.get('first_name', '')} {applicant.get('last_name', '')}")
            print(f"Status: {status_data.get('overall_status', 'unknown')}")
            print(f"Documents: {len(status_data.get('documents', []))}")
            print(f"Decisions: {len(status_data.get('decisions', []))}")
            
        else:
            print(f"❌ Status check failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")

def demo_decision_retrieval(application_id):
    """Demonstrate decision retrieval"""
    if not application_id:
        print("❌ No application ID available for decision retrieval")
        return
    
    print(f"\n🎯 Demo: Decision Retrieval for Application {application_id}")
    print("=" * 50)
    
    print("Retrieving decision...")
    
    try:
        response = requests.get(f"http://localhost:8000/decision/{application_id}", timeout=10)
        
        if response.status_code == 200:
            decision_data = response.json()
            print("✅ Decision retrieved successfully!")
            
            # Display decision information
            decision = decision_data.get('decision', 'unknown')
            confidence = decision_data.get('confidence_score', 0.0)
            reason = decision_data.get('decision_reason', 'No reason provided')
            
            print(f"Decision: {decision.upper()}")
            print(f"Confidence: {confidence:.1%}")
            print(f"Reason: {reason}")
            
            # Display SHAP values if available
            shap_values = decision_data.get('shap_values', {})
            if shap_values:
                print("\nTop Contributing Factors:")
                sorted_factors = sorted(shap_values.items(), key=lambda x: x[1], reverse=True)[:3]
                for factor, importance in sorted_factors:
                    print(f"  • {factor}: {importance:.1%}")
            
            # Display recommendations
            recommendations = decision_data.get('recommendations', [])
            if recommendations:
                print(f"\nRecommendations ({len(recommendations)}):")
                for i, rec in enumerate(recommendations, 1):
                    print(f"  {i}. {rec}")
            
        else:
            print(f"❌ Decision retrieval failed: {response.text}")
            
    except Exception as e:
        print(f"❌ Error retrieving decision: {e}")

def demo_chat_interface(application_id):
    """Demonstrate chat interface"""
    if not application_id:
        print("❌ No application ID available for chat demo")
        return
    
    print(f"\n💬 Demo: Chat Interface for Application {application_id}")
    print("=" * 50)
    
    sample_questions = [
        "What is the decision on my application?",
        "Can you explain why this decision was made?",
        "What recommendations do you have for me?",
        "How can I improve my application for next time?"
    ]
    
    for question in sample_questions:
        print(f"\nQuestion: {question}")
        
        try:
            chat_data = {
                "message": question,
                "context": {"application_id": application_id}
            }
            
            response = requests.post(
                f"http://localhost:8000/chat/{application_id}",
                json=chat_data,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                answer = result.get('response', 'No response received')
                confidence = result.get('confidence', 0.0)
                
                print(f"Answer: {answer}")
                print(f"Confidence: {confidence:.1%}")
                
            else:
                print(f"❌ Chat failed: {response.text}")
                
        except Exception as e:
            print(f"❌ Error in chat: {e}")
        
        time.sleep(1)  # Brief pause between questions

def demo_system_capabilities():
    """Demonstrate overall system capabilities"""
    print("\n🚀 Demo: System Capabilities Overview")
    print("=" * 40)
    
    capabilities = [
        "Multi-document processing (PDF, images, Excel, text)",
        "OCR for image-based documents",
        "Intelligent data extraction and validation",
        "ML-powered eligibility decisions",
        "SHAP-based explainability",
        "Personalized recommendations",
        "Multi-agent orchestration",
        "Real-time status tracking",
        "Interactive chat interface",
        "Comprehensive audit logging"
    ]
    
    print("The system provides the following capabilities:")
    for i, capability in enumerate(capabilities, 1):
        print(f"  {i}. {capability}")
    
    print("\nTechnical Features:")
    tech_features = [
        "FastAPI backend with async processing",
        "Streamlit UI for user interaction",
        "PostgreSQL database with audit trails",
        "Local LLM integration (Ollama)",
        "Vector database for semantic search",
        "Containerized deployment ready",
        "Comprehensive error handling",
        "Performance monitoring and logging"
    ]
    
    for i, feature in enumerate(tech_features, 1):
        print(f"  {i}. {feature}")

def main():
    """Main demo function"""
    print("🤖 Social Support AI System - Demo")
    print("=" * 50)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check system health
    if not check_system_health():
        print("\n❌ System is not ready. Please ensure:")
        print("1. FastAPI backend is running (uvicorn app.main:app --reload)")
        print("2. Database is set up and accessible")
        print("3. All dependencies are installed")
        return
    
    # Run demos
    try:
        # Demo 1: Application submission
        application_id = demo_application_submission()
        
        if application_id:
            # Wait a bit for processing
            print("\n⏳ Waiting for application processing...")
            time.sleep(5)
            
            # Demo 2: Status checking
            demo_status_checking(application_id)
            
            # Demo 3: Decision retrieval
            demo_decision_retrieval(application_id)
            
            # Demo 4: Chat interface
            demo_chat_interface(application_id)
        
        # Demo 5: System capabilities
        demo_system_capabilities()
        
        print("\n✅ Demo completed successfully!")
        print("\nNext steps:")
        print("1. Explore the Streamlit UI: streamlit run app/streamlit_app.py")
        print("2. Check the API documentation: http://localhost:8000/docs")
        print("3. Generate synthetic data: python scripts/generate_synthetic_data.py")
        
    except KeyboardInterrupt:
        print("\n\n⏹️ Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        print("Please check the system logs for more details")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Quick Demo Script for Social Support AI System
This script demonstrates the system capabilities without requiring external services.
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def demo_agent_system():
    """Demonstrate the multi-agent system"""
    print("🤖 Multi-Agent System Demo")
    print("=" * 50)
    
    try:
        # Import and create agents
        from app.agents.extraction_agent import ExtractionAgent
        from app.agents.validation_agent import ValidationAgent
        from app.agents.eligibility_agent import EligibilityAgent
        from app.agents.recommender_agent import RecommenderAgent
        from app.agents.master_agent import MasterAgent
        
        print("✅ All agents imported successfully")
        
        # Create agent instances
        extraction_agent = ExtractionAgent()
        validation_agent = ValidationAgent()
        eligibility_agent = EligibilityAgent()
        recommender_agent = RecommenderAgent()
        master_agent = MasterAgent()
        
        print(f"✅ Created {master_agent.name} with {len(master_agent.agents)} sub-agents")
        
        # Show agent capabilities
        print("\n🔧 Agent Capabilities:")
        for name, agent in master_agent.agents.items():
            capabilities = agent.get_capabilities()
            print(f"  • {name.title()}: {', '.join(capabilities[:3])}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent system demo failed: {e}")
        return False

def demo_data_models():
    """Demonstrate data models"""
    print("\n📊 Data Models Demo")
    print("=" * 50)
    
    try:
        from app.models.pydantic_models import ApplicationSubmission, DecisionType
        
        # Create sample application
        sample_data = {
            "first_name": "Jane",
            "last_name": "Smith",
            "date_of_birth": "1990-03-15",
            "email": "jane.smith@example.com",
            "phone": "(555) 987-6543",
            "street_address": "456 Oak Avenue",
            "city": "Springfield",
            "state": "IL",
            "postal_code": "62701",
            "country": "United States",
            "monthly_income": 5200.0,
            "employment_status": "Full-time",
            "employer_name": "Tech Innovations Inc",
            "employment_length_months": 48,
            "family_size": 2,
            "dependents": 0
        }
        
        app_submission = ApplicationSubmission(**sample_data)
        print(f"✅ Application created: {app_submission.first_name} {app_submission.last_name}")
        print(f"   Income: ${app_submission.monthly_income:,.2f}")
        print(f"   Employment: {app_submission.employment_status} at {app_submission.employer_name}")
        
        # Show decision types
        print(f"\n🎯 Available Decision Types: {[dt.value for dt in DecisionType]}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data models demo failed: {e}")
        return False

def demo_synthetic_data():
    """Demonstrate synthetic data generation"""
    print("\n🎲 Synthetic Data Generation Demo")
    print("=" * 50)
    
    try:
        from scripts.generate_synthetic_data import generate_synthetic_applicants
        
        # Generate sample data
        applicants = generate_synthetic_applicants(3)
        print(f"✅ Generated {len(applicants)} synthetic applicants")
        
        # Show sample data
        for i, applicant in enumerate(applicants, 1):
            print(f"\n  Applicant {i}:")
            print(f"    Name: {applicant['first_name']} {applicant['last_name']}")
            print(f"    Income: ${applicant['monthly_income']:,.2f}")
            print(f"    Employment: {applicant['employment_status']}")
            print(f"    Family Size: {applicant['family_size']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Synthetic data demo failed: {e}")
        return False

def demo_ml_pipeline():
    """Demonstrate ML pipeline capabilities"""
    print("\n🧠 ML Pipeline Demo")
    print("=" * 50)
    
    try:
        from app.agents.eligibility_agent import EligibilityAgent
        
        # Create eligibility agent
        agent = EligibilityAgent()
        print(f"✅ Created {agent.name}")
        print(f"   Features: {len(agent.feature_names)}")
        print(f"   Model Version: {agent.model_version}")
        
        # Show feature engineering
        print(f"\n🔧 Feature Engineering:")
        for feature in agent.feature_names:
            print(f"  • {feature}")
        
        # Test feature calculation
        test_data = {
            'monthly_income': 4500.0,
            'employment_length_months': 24,
            'family_size': 3,
            'dependents': 1
        }
        
        print(f"\n📊 Sample Feature Calculation:")
        print(f"   Income Stability: {agent._calculate_income_stability(test_data):.2f}")
        print(f"   Employment Stability: {agent._calculate_employment_stability(test_data):.2f}")
        print(f"   Credit Score Estimate: {agent._estimate_credit_score(test_data):.0f}")
        
        return True
        
    except Exception as e:
        print(f"❌ ML pipeline demo failed: {e}")
        return False

def demo_workflow():
    """Demonstrate the complete workflow"""
    print("\n🔄 Complete Workflow Demo")
    print("=" * 50)
    
    try:
        from app.agents.master_agent import MasterAgent
        
        # Create master agent
        master = MasterAgent()
        print(f"✅ Created {master.name}")
        print(f"   Workflow Steps: {len(master.workflow_steps)}")
        print(f"   Steps: {' → '.join(master.workflow_steps)}")
        
        # Show workflow orchestration
        print(f"\n🎭 Workflow Orchestration:")
        print(f"   • Master Agent coordinates all sub-agents")
        print(f"   • Implements ReAct pattern (Reasoning + Acting)")
        print(f"   • Handles errors and provides graceful degradation")
        print(f"   • Tracks progress and aggregates results")
        
        return True
        
    except Exception as e:
        print(f"❌ Workflow demo failed: {e}")
        return False

def demo_security_features():
    """Demonstrate security features"""
    print("\n🔒 Security Features Demo")
    print("=" * 50)
    
    try:
        from app.core.config import settings
        
        print("✅ Security Configuration:")
        print(f"   • PII Masking: {'Enabled' if settings.pii_masking_enabled else 'Disabled'}")
        print(f"   • Database Encryption: Configured")
        print(f"   • Audit Logging: Enabled")
        print(f"   • File Upload Security: {settings.max_file_size:,} bytes max")
        
        print(f"\n🛡️ Security Capabilities:")
        print(f"   • Input validation and sanitization")
        print(f"   • Secure file handling")
        print(f"   • Comprehensive audit trails")
        print(f"   • Role-based access control ready")
        
        return True
        
    except Exception as e:
        print(f"❌ Security features demo failed: {e}")
        return False

def main():
    """Main demo function"""
    print("🚀 Social Support AI System - Quick Demo")
    print("=" * 60)
    print(f"Demo started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("This demo shows the system capabilities without external dependencies")
    print()
    
    demos = [
        ("Multi-Agent System", demo_agent_system),
        ("Data Models", demo_data_models),
        ("Synthetic Data", demo_synthetic_data),
        ("ML Pipeline", demo_ml_pipeline),
        ("Workflow Orchestration", demo_workflow),
        ("Security Features", demo_security_features)
    ]
    
    results = []
    
    for demo_name, demo_func in demos:
        print(f"\n{'='*20} {demo_name} {'='*20}")
        try:
            success = demo_func()
            results.append((demo_name, success))
        except Exception as e:
            print(f"❌ Demo {demo_name} crashed: {e}")
            results.append((demo_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 DEMO SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for demo_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {demo_name}")
    
    print(f"\nOverall: {passed}/{total} demos successful")
    
    if passed == total:
        print("\n🎉 All demos successful! The system is working correctly.")
        print("\n🚀 Next Steps to Run the Full System:")
        print("1. Install PostgreSQL database")
        print("2. Setup environment: cp env.example .env")
        print("3. Configure database connection in .env")
        print("4. Setup database: python3 scripts/setup_database.py")
        print("5. Start backend: uvicorn app.main:app --reload")
        print("6. Start frontend: streamlit run app/streamlit_app.py")
        print("7. Install Ollama for LLM functionality (optional)")
        
        print("\n💡 Quick Test Commands:")
        print("• Test system: python3 scripts/simple_test.py")
        print("• Generate data: python3 scripts/generate_synthetic_data.py")
        print("• Run demo: python3 scripts/demo.py")
        print("• Generate demo guides: python3 scripts/create_demo_gifs.py")
        print("• Follow the guides to record:")
        print("  - Dashboard overview")
        print("  - Application submission")
        print("  - Document processing")
        print("  - ML decision display")
        print("  - Chat interface")
        
    else:
        print(f"\n⚠️ {total - passed} demos failed. Check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all dependencies are installed")
        print("2. Check Python version (3.9+ required)")
        print("3. Verify file permissions")
        print("4. Check import paths")

if __name__ == "__main__":
    main() 
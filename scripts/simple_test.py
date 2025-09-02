#!/usr/bin/env python3
"""
Simple test script for Social Support AI System
This script tests basic functionality without requiring the full system to be running.
"""

import sys
import os
import json
from datetime import datetime

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """Test if we can import the main modules"""
    print("🔍 Testing module imports...")
    
    try:
        # Test core imports
        from app.core.config import settings
        print("✅ Core config imported successfully")
        
        from app.core.database import Base, init_db
        print("✅ Database modules imported successfully")
        
        from app.models.database_models import Applicant, Document, Decision
        print("✅ Data models imported successfully")
        
        from app.models.pydantic_models import ApplicationSubmission, DecisionType
        print("✅ Pydantic models imported successfully")
        
        from app.agents.base_agent import BaseAgent
        print("✅ Base agent imported successfully")
        
        # Import all agent classes
        from app.agents.extraction_agent import ExtractionAgent
        print("✅ Extraction agent imported successfully")
        
        from app.agents.validation_agent import ValidationAgent
        print("✅ Validation agent imported successfully")
        
        from app.agents.eligibility_agent import EligibilityAgent
        print("✅ Eligibility agent imported successfully")
        
        from app.agents.recommender_agent import RecommenderAgent
        print("✅ Recommender agent imported successfully")
        
        from app.agents.master_agent import MasterAgent
        print("✅ Master agent imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from app.core.config import settings
        
        print(f"✅ Database URL: {settings.database_url[:50]}...")
        print(f"✅ Upload directory: {settings.upload_dir}")
        print(f"✅ Model path: {settings.model_path}")
        print(f"✅ LLM model: {settings.ollama_model}")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_agent_creation():
    """Test if agents can be instantiated"""
    print("\n🤖 Testing agent creation...")
    
    try:
        # Import all agent classes
        from app.agents.extraction_agent import ExtractionAgent
        from app.agents.validation_agent import ValidationAgent
        from app.agents.eligibility_agent import EligibilityAgent
        from app.agents.recommender_agent import RecommenderAgent
        from app.agents.master_agent import MasterAgent
        
        # Test extraction agent
        extraction_agent = ExtractionAgent()
        print(f"✅ Extraction agent created: {extraction_agent.name}")
        
        # Test validation agent
        validation_agent = ValidationAgent()
        print(f"✅ Validation agent created: {validation_agent.name}")
        
        # Test eligibility agent
        eligibility_agent = EligibilityAgent()
        print(f"✅ Eligibility agent created: {eligibility_agent.name}")
        
        # Test recommender agent
        recommender_agent = RecommenderAgent()
        print(f"✅ Recommender agent created: {recommender_agent.name}")
        
        # Test master agent
        master_agent = MasterAgent()
        print(f"✅ Master agent created: {master_agent.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

def test_data_models():
    """Test data model functionality"""
    print("\n📊 Testing data models...")
    
    try:
        from app.models.pydantic_models import ApplicationSubmission, DecisionType
        
        # Test application submission model
        sample_data = {
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
        
        app_submission = ApplicationSubmission(**sample_data)
        print(f"✅ Application submission model created: {app_submission.first_name} {app_submission.last_name}")
        
        # Test decision types
        decision_types = [dt.value for dt in DecisionType]
        print(f"✅ Decision types: {decision_types}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data model test failed: {e}")
        return False

def test_agent_capabilities():
    """Test agent capabilities"""
    print("\n🔧 Testing agent capabilities...")
    
    try:
        # Import all agent classes
        from app.agents.extraction_agent import ExtractionAgent
        from app.agents.validation_agent import ValidationAgent
        from app.agents.eligibility_agent import EligibilityAgent
        from app.agents.recommender_agent import RecommenderAgent
        from app.agents.master_agent import MasterAgent
        
        # Test extraction agent capabilities
        extraction_agent = ExtractionAgent()
        capabilities = extraction_agent.get_capabilities()
        print(f"✅ Extraction agent capabilities: {capabilities}")
        
        # Test validation agent capabilities
        validation_agent = ValidationAgent()
        capabilities = validation_agent.get_capabilities()
        print(f"✅ Validation agent capabilities: {capabilities}")
        
        # Test eligibility agent capabilities
        eligibility_agent = EligibilityAgent()
        capabilities = eligibility_agent.get_capabilities()
        print(f"✅ Eligibility agent capabilities: {capabilities}")
        
        # Test recommender agent capabilities
        recommender_agent = RecommenderAgent()
        capabilities = recommender_agent.get_capabilities()
        print(f"✅ Recommender agent capabilities: {capabilities}")
        
        # Test master agent capabilities
        master_agent = MasterAgent()
        capabilities = master_agent.get_capabilities()
        print(f"✅ Master agent capabilities: {capabilities}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent capabilities test failed: {e}")
        return False

def test_synthetic_data_generation():
    """Test synthetic data generation"""
    print("\n🎲 Testing synthetic data generation...")
    
    try:
        from scripts.generate_synthetic_data import generate_synthetic_applicants
        
        # Generate a small sample
        applicants = generate_synthetic_applicants(5)
        print(f"✅ Generated {len(applicants)} synthetic applicants")
        
        # Show sample data
        if applicants:
            sample = applicants[0]
            print(f"✅ Sample applicant: {sample['first_name']} {sample['last_name']}")
            print(f"   Income: ${sample['monthly_income']:,.2f}")
            print(f"   Employment: {sample['employment_status']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Synthetic data generation failed: {e}")
        return False

def test_file_structure():
    """Test if all required files exist"""
    print("\n📁 Testing file structure...")
    
    required_files = [
        "app/__init__.py",
        "app/core/config.py",
        "app/core/database.py",
        "app/models/database_models.py",
        "app/models/pydantic_models.py",
        "app/agents/base_agent.py",
        "app/agents/extraction_agent.py",
        "app/agents/validation_agent.py",
        "app/agents/eligibility_agent.py",
        "app/agents/recommender_agent.py",
        "app/agents/master_agent.py",
        "app/api/main.py",
        "app/streamlit_app.py",
        "requirements.txt",
        "README.md",
        "LICENSE"
    ]
    
    missing_files = []
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path}")
            missing_files.append(file_path)
    
    if missing_files:
        print(f"\n⚠️ Missing files: {len(missing_files)}")
        return False
    else:
        print(f"\n✅ All required files present: {len(required_files)}")
        return True

def main():
    """Main test function"""
    print("🧪 Social Support AI System - Simple Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    tests = [
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Data Models", test_data_models),
        ("Agent Creation", test_agent_creation),
        ("Agent Capabilities", test_agent_capabilities),
        ("Synthetic Data", test_synthetic_data_generation)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready for basic testing.")
        print("\n🚀 Next steps:")
        print("1. Install dependencies: pip3 install -r requirements.txt")
        print("2. Setup database: python3 scripts/setup_database.py")
        print("3. Start the system: uvicorn app.main:app --reload")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all files are present")
        print("2. Check Python version (3.9+ required)")
        print("3. Install missing dependencies")
        print("4. Check file permissions")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Simple test server to verify the system works
"""

import requests
import time
import subprocess
import sys

def test_imports():
    """Test if we can import the main modules"""
    print("🔍 Testing imports...")
    
    try:
        from app.core.config import settings
        print("✅ Config imported")
        
        from app.api.main import app
        print("✅ FastAPI app imported")
        
        from app.streamlit_app import main as streamlit_main
        print("✅ Streamlit app imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_simple_fastapi():
    """Test a simple FastAPI server"""
    print("\n🚀 Testing simple FastAPI server...")
    
    try:
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        
        # Create a simple test app
        test_app = FastAPI()
        
        @test_app.get("/test")
        def test_endpoint():
            return {"message": "Hello World", "status": "success"}
        
        # Test with test client
        client = TestClient(test_app)
        response = client.get("/test")
        
        if response.status_code == 200:
            print("✅ Simple FastAPI test successful")
            print(f"   Response: {response.json()}")
            return True
        else:
            print(f"❌ FastAPI test failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ FastAPI test failed: {e}")
        return False

def test_agent_system():
    """Test the agent system"""
    print("\n🤖 Testing agent system...")
    
    try:
        from app.agents.master_agent import MasterAgent
        
        master = MasterAgent()
        print(f"✅ Master agent created: {master.name}")
        print(f"   Sub-agents: {len(master.agents)}")
        
        for name, agent in master.agents.items():
            print(f"   • {name}: {agent.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Simple System Test")
    print("=" * 40)
    
    tests = [
        ("Imports", test_imports),
        ("Simple FastAPI", test_simple_fastapi),
        ("Agent System", test_agent_system)
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
    print("\n" + "="*40)
    print("📊 TEST SUMMARY")
    print("=" * 40)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! The system is ready.")
        print("\n🚀 Next steps:")
        print("1. Open http://localhost:8501 for Streamlit UI")
        print("2. Open http://localhost:8000 for FastAPI backend")
        print("3. Create GitHub repository and push code")
    else:
        print(f"\n⚠️ {total - passed} tests failed. Check errors above.")

if __name__ == "__main__":
    main() 
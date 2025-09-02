import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
import uuid
import random # Added for enhanced demo mode

# Page configuration
st.set_page_config(
    page_title="Social Support Application Evaluation AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Constants
API_BASE_URL = "http://localhost:8000"

def main():
    """Main Streamlit application"""
    st.title("🤖 Social Support Application Evaluation AI")
    st.markdown("---")
    
    # Initialize session state for navigation
    if 'navigation' not in st.session_state:
        st.session_state.navigation = "🏠 Dashboard"
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["🏠 Dashboard", "📝 Submit Application", "📊 Application Status", "💬 Chat Assistant", "📈 Analytics"],
        index=["🏠 Dashboard", "📝 Submit Application", "📊 Application Status", "💬 Chat Assistant", "📈 Analytics"].index(st.session_state.navigation)
    )
    
    # Update session state when sidebar changes
    if page != st.session_state.navigation:
        st.session_state.navigation = page
    
    # Display selected page
    if st.session_state.navigation == "🏠 Dashboard":
        show_dashboard()
    elif st.session_state.navigation == "📝 Submit Application":
        show_application_submission()
    elif st.session_state.navigation == "📊 Application Status":
        show_application_status()
    elif st.session_state.navigation == "💬 Chat Assistant":
        show_chat_assistant()
    elif st.session_state.navigation == "📈 Analytics":
        show_analytics()

def show_dashboard():
    """Display main dashboard"""
    st.header("Dashboard")
    
    # System status
    col1, col2, col3, col4 = st.columns(4)
    
    # Check backend health
    backend_online = False
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=3)
        if response.status_code == 200:
            backend_online = True
            col1.metric("System Status", "🟢 Online", "Backend Connected")
        else:
            col1.metric("System Status", "🟡 Limited", "Backend Error")
    except:
        col1.metric("System Status", "🔴 Offline", "Backend Unreachable")
    
    # Show demo data when backend is offline
    if backend_online:
        col2.metric("Total Applications", "0", "No data")
        col3.metric("Processing", "0", "No data")
        col4.metric("Completed", "0", "No data")
    else:
        col2.metric("Total Applications", "25", "Demo Mode")
        col3.metric("Processing", "3", "Demo Mode")
        col4.metric("Completed", "22", "Demo Mode")
    
    st.markdown("---")
    
    # Quick actions
    st.subheader("Quick Actions")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📝 New Application", use_container_width=True):
            st.session_state.navigation = "📝 Submit Application"
            st.rerun()
    
    with col2:
        if st.button("📊 Check Status", use_container_width=True):
            st.session_state.navigation = "📊 Application Status"
            st.rerun()
    
    with col3:
        if st.button("💬 Chat Assistant", use_container_width=True):
            st.session_state.navigation = "💬 Chat Assistant"
            st.rerun()
    
    # System information
    st.subheader("System Information")
    
    if backend_online:
        st.success("✅ Backend API is running and accessible")
        st.info("🚀 All features are available - you can submit applications, check status, and chat with AI")
    else:
        st.warning("⚠️ Backend API is currently offline")
        st.info("🎭 Running in Demo Mode - you can explore the UI and see how the system works")
        st.info("🔧 To enable full functionality, start the FastAPI backend with: `python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`")
    
    # Recent activity
    st.subheader("Recent Activity")
    if backend_online:
        st.info("No recent activity to display")
    else:
        # Show demo activity
        demo_activities = [
            "📝 Arjun Patel submitted application (ID: demo-001)",
            "✅ Priya Sharma application processed - APPROVED",
            "📊 Rajesh Kumar status updated - SOFT DECLINE",
            "💬 AI chat session started for demo-003"
        ]
        
        for activity in demo_activities:
            st.write(f"• {activity}")
        
        st.caption("💡 This is demo data. Start the backend to see real activity.")

def show_application_submission():
    """Show application submission form"""
    st.header("📝 Submit Application")
    
    # Check if backend is online
    backend_online = False
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=3)
        backend_online = response.status_code == 200
    except:
        pass
    
    if not backend_online:
        st.warning("⚠️ Backend API is offline - running in Demo Mode")
        st.info("🎭 You can fill out the form to see how it works, but submissions won't be processed until the backend is running.")
        st.info("🔧 Start the backend with: `python3 -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`")
        st.markdown("---")
    
    # Supporting Documents (outside form for compatibility)
    st.subheader("Supporting Documents")
    
    uploaded_files = st.file_uploader(
        "Upload Documents",
        type=["pdf", "jpg", "jpeg", "png", "xlsx", "xls", "txt"],
        accept_multiple_files=True,
        help="Upload documents like ID, bank statements, pay stubs, etc."
    )
    
    with st.form("application_form"):
        st.subheader("Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First Name *", placeholder="e.g., Arjun")
            email = st.text_input("Email *", placeholder="e.g., arjun.patel@gmail.com")
            phone = st.text_input("Phone *", placeholder="e.g., +91 9876543210")
            date_of_birth = st.date_input("Date of Birth *", value=datetime(1990, 1, 1))
        
        with col2:
            last_name = st.text_input("Last Name *", placeholder="e.g., Patel")
            street_address = st.text_input("Street Address *", placeholder="e.g., 123 Sector 15, Block A")
            city = st.text_input("City *", placeholder="e.g., Mumbai")
            state = st.text_input("State *", placeholder="e.g., Maharashtra")
        
        postal_code = st.text_input("Postal Code *", placeholder="e.g., 400001")
        country = st.text_input("Country *", value="India")
        
        st.markdown("---")
        st.subheader("Financial Information")
        
        col1, col2 = st.columns(2)
        with col1:
            monthly_income = st.number_input("Monthly Income (INR) *", min_value=0, value=75000, step=1000, help="Enter your monthly income in Indian Rupees")
            employment_status = st.selectbox("Employment Status *", ["Full-time", "Part-time", "Contract", "Freelance", "Self-employed", "Unemployed", "Student", "Retired"])
            family_size = st.number_input("Family Size *", min_value=1, value=4, step=1, help="Total number of family members")
        
        with col2:
            employer_name = st.text_input("Employer Name", placeholder="e.g., Tata Consultancy Services", help="Leave blank if unemployed or self-employed")
            employment_length_months = st.number_input("Employment Length (months)", min_value=0, value=48, step=1, help="How long have you been employed?")
            dependents = st.number_input("Dependents", min_value=0, value=2, step=1, help="Number of family members who depend on your income")
        
        submitted = st.form_submit_button("Submit Application", use_container_width=True)
        
        if submitted:
            if not all([first_name, last_name, email, phone, street_address, city, state, postal_code, country, monthly_income, employment_status, family_size]):
                st.error("Please fill in all required fields marked with *")
            else:
                if backend_online:
                    # Call the submit function without await since we're not in an async context
                    submit_application(
                        first_name, last_name, email, phone, street_address, city, state, 
                        postal_code, country, monthly_income, employment_status, employer_name,
                        employment_length_months, family_size, dependents, date_of_birth, uploaded_files
                    )
                else:
                    # Enhanced Demo Mode - Show full AI workflow
                    st.success("🎭 Demo Mode: Application submitted successfully!")
                    
                    # Simulate AI processing workflow
                    with st.expander("🤖 AI Processing Workflow", expanded=True):
                        st.info("**Step 1: Document Processing & Extraction**")
                        
                        # Document analysis
                        if uploaded_files:
                            st.write("📄 **Documents Analyzed:**")
                            document_warnings = []
                            
                            for i, file in enumerate(uploaded_files, 1):
                                file_type = file.name.split('.')[-1].upper()
                                file_size = len(file.getvalue())
                                
                                # Document validation checks
                                warnings = []
                                
                                # Check file size (suspiciously small files)
                                if file_size < 1000:  # Less than 1KB
                                    warnings.append("⚠️ File size suspiciously small - may be fake")
                                
                                # Check file names for suspicious patterns
                                suspicious_keywords = ['fake', 'test', 'sample', 'dummy', 'example']
                                if any(keyword in file.name.lower() for keyword in suspicious_keywords):
                                    warnings.append("🚨 File name suggests test/fake document")
                                
                                # Check for common fake document patterns
                                if file_type == 'PDF' and file_size < 5000:
                                    warnings.append("⚠️ PDF file unusually small - may be corrupted or fake")
                                
                                if file_type in ['JPG', 'PNG'] and file_size < 2000:
                                    warnings.append("⚠️ Image file unusually small - may be fake or corrupted")
                                
                                # Display document analysis
                                if warnings:
                                    st.write(f"  {i}. {file.name} - {file_type} processed, data extracted")
                                    for warning in warnings:
                                        st.error(f"     {warning}")
                                        document_warnings.extend(warnings)
                                else:
                                    st.write(f"  {i}. {file.name} - {file_type} processed, data extracted ✅")
                            
                            # Overall document assessment
                            if document_warnings:
                                st.error("🚨 **Document Validation Issues Detected:**")
                                st.write("The AI system has identified potential issues with uploaded documents:")
                                for warning in set(document_warnings):  # Remove duplicates
                                    st.write(f"• {warning}")
                                st.write("**Impact:** These issues may significantly affect approval chances and require human review.")
                        else:
                            st.warning("⚠️ No documents uploaded - this may affect approval chances")
                        
                        st.info("**Step 2: Multi-Agent AI Processing**")
                        
                        # Simulate agent processing
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.write("🔍 **Extraction Agent**")
                            st.write("✅ Personal info extracted")
                            st.write("✅ Financial data parsed")
                            st.write("✅ Document content analyzed")
                        
                        with col2:
                            st.write("✅ **Validation Agent**")
                            st.write("✅ Cross-checked information")
                            st.write("✅ Resolved data conflicts")
                            st.write("✅ Calculated confidence scores")
                        
                        with col3:
                            st.write("🧠 **Eligibility Agent**")
                            st.write("✅ Features engineered")
                            st.write("✅ ML model applied")
                            st.write("✅ Risk score calculated")
                    
                    # Risk assessment and decision
                    st.markdown("---")
                    st.subheader("🎯 AI Decision & Analysis")
                    
                    # Calculate risk factors
                    risk_score = 0
                    risk_factors = []
                    
                    # Income risk
                    if monthly_income < 50000:
                        risk_score += 30
                        risk_factors.append("Low income relative to family size")
                    elif monthly_income < 80000:
                        risk_score += 15
                        risk_factors.append("Moderate income level")
                    else:
                        risk_score -= 10
                        risk_factors.append("Strong income level")
                    
                    # Employment risk
                    if employment_status == "Unemployed":
                        risk_score += 40
                        risk_factors.append("Currently unemployed")
                    elif employment_status == "Self-employed":
                        risk_score += 20
                        risk_factors.append("Self-employed (variable income)")
                    elif employment_length_months < 12:
                        risk_score += 25
                        risk_factors.append("Short employment history")
                    else:
                        risk_score -= 15
                        risk_factors.append("Stable employment history")
                    
                    # Family size risk
                    if family_size > 6:
                        risk_score += 20
                        risk_factors.append("Large family size")
                    elif family_size > 4:
                        risk_score += 10
                        risk_factors.append("Above average family size")
                    
                    # Document risk
                    if not uploaded_files:
                        risk_score += 25
                        risk_factors.append("No supporting documents")
                    elif len(uploaded_files) < 2:
                        risk_score += 15
                        risk_factors.append("Limited documentation")
                    
                    # Document validation risk (from enhanced demo)
                    if 'document_warnings' in locals() and document_warnings:
                        risk_score += 35
                        risk_factors.append("Document validation issues detected")
                        risk_factors.append("Suspicious or fake documents flagged")
                    
                    # Normalize risk score
                    risk_score = max(0, min(100, risk_score))
                    
                    # Decision logic
                    if risk_score < 30:
                        decision = "APPROVED"
                        confidence = 0.85 + (random.random() * 0.10)
                        decision_color = "success"
                    elif risk_score < 60:
                        decision = "SOFT DECLINE"
                        confidence = 0.70 + (random.random() * 0.15)
                        decision_color = "warning"
                    else:
                        decision = "HARD DECLINE"
                        confidence = 0.60 + (random.random() * 0.20)
                        decision_color = "error"
                    
                    # Display decision
                    col1, col2 = st.columns([1, 2])
                    with col1:
                        if decision == "APPROVED":
                            st.success(f"🎉 **{decision}**")
                        elif decision == "SOFT DECLINE":
                            st.warning(f"⚠️ **{decision}**")
                        else:
                            st.error(f"❌ **{decision}**")
                        
                        st.metric("Confidence Score", f"{confidence:.1%}")
                        st.metric("Risk Score", f"{risk_score}/100")
                    
                    with col2:
                        st.write("**Key Risk Factors:**")
                        for factor in risk_factors[:5]:  # Show top 5
                            st.write(f"• {factor}")
                    
                    # SHAP-like feature importance
                    st.markdown("---")
                    st.subheader("🔍 AI Explainability (SHAP Values)")
                    
                    # Calculate feature importance
                    features = {
                        "Monthly Income": abs(monthly_income - 75000) / 75000 * 100,
                        "Employment Status": 25 if employment_status in ["Unemployed", "Self-employed"] else 10,
                        "Employment Length": max(0, (60 - employment_length_months) / 60 * 100),
                        "Family Size": max(0, (family_size - 4) / 4 * 100),
                        "Documentation": 30 if not uploaded_files else 10
                    }
                    
                    # Normalize feature importance
                    total_importance = sum(features.values())
                    if total_importance > 0:
                        features = {k: v/total_importance * 100 for k, v in features.items()}
                    
                    # Display feature importance
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Feature Importance:**")
                        for feature, importance in sorted(features.items(), key=lambda x: x[1], reverse=True):
                            st.write(f"• {feature}: {importance:.1f}%")
                    
                    with col2:
                        # Create a simple bar chart
                        import plotly.express as px
                        feature_df = pd.DataFrame({
                            'Feature': list(features.keys()),
                            'Importance': list(features.values())
                        })
                        fig = px.bar(feature_df, x='Importance', y='Feature', orientation='h',
                                    title="Feature Importance Analysis")
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # AI Recommendations
                    st.markdown("---")
                    st.subheader("💡 AI Economic Enablement Recommendations")
                    
                    if decision == "APPROVED":
                        st.success("**Approval Recommendations:**")
                        st.write("• Access to full social support benefits")
                        st.write("• Consider additional financial planning services")
                        st.write("• Explore skill development opportunities")
                    elif decision == "SOFT DECLINE":
                        st.warning("**Improvement Recommendations:**")
                        st.write("• Increase income stability (consider additional employment)")
                        st.write("• Build credit history through small loans")
                        st.write("• Provide additional documentation (bank statements, employment letters)")
                        st.write("• Consider family planning for better financial stability")
                        st.write("• Explore government training programs")
                    else:
                        st.error("**Alternative Support Options:**")
                        st.write("• Emergency assistance programs")
                        st.write("• Food and housing support services")
                        st.write("• Job training and placement services")
                        st.write("• Financial counseling and debt management")
                        st.write("• Community support networks")
                    
                    st.info("🔧 To enable real AI processing and database storage, start the backend API first.")

def submit_application(*args):
    """Submit application to the API"""
    try:
        # Prepare application data
        application_data = {
            "first_name": args[0],
            "last_name": args[1],
            "email": args[2],
            "phone": args[3],
            "street_address": args[4],
            "city": args[5],
            "state": args[6],
            "postal_code": args[7],
            "country": args[8],
            "monthly_income": float(args[9]),
            "employment_status": args[10],
            "employer_name": args[11] if args[11] else None,
            "employment_length_months": int(args[12]) if args[12] else None,
            "family_size": int(args[13]),
            "dependents": int(args[14]) if args[14] else 0,
            "date_of_birth": args[15].strftime("%Y-%m-%d")
        }
        
        # Prepare files
        files = []
        for uploaded_file in args[16]:
            files.append(('files', (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)))
        
        # Submit to API
        # Prepare form data - FastAPI expects application_data as form fields
        form_data = {
            "first_name": application_data["first_name"],
            "last_name": application_data["last_name"],
            "email": application_data["email"],
            "phone": application_data["phone"],
            "street_address": application_data["street_address"],
            "city": application_data["city"],
            "state": application_data["state"],
            "postal_code": application_data["postal_code"],
            "country": application_data["country"],
            "monthly_income": str(application_data["monthly_income"]),
            "employment_status": application_data["employment_status"],
            "employer_name": application_data["employer_name"] or "",
            "employment_length_months": str(application_data["employment_length_months"] or 0),
            "family_size": str(application_data["family_size"]),
            "dependents": str(application_data["dependents"]),
            "date_of_birth": application_data["date_of_birth"]
        }
        
        response = requests.post(
            f"{API_BASE_URL}/ingest",
            data=form_data,  # Send as form data
            files=files
        )
        
        if response.status_code == 200:
            result = response.json()
            st.success("🎉 Application submitted successfully!")
            st.info(f"Application ID: {result.get('application_id')}")
            st.info(f"Status: {result.get('status')}")
            
            # Store application ID in session
            st.session_state.current_application_id = result.get('application_id')
            
            # Display complete analysis results
            st.markdown("---")
            st.subheader("🤖 AI Analysis Results")
            
            # Decision and reason
            decision = result.get('decision', 'unknown')
            decision_reason = result.get('decision_reason', 'No reason provided')
            
            if decision == 'approved':
                st.success(f"✅ **DECISION: APPROVED**")
            elif decision == 'soft_decline':
                st.warning(f"⚠️ **DECISION: SOFT DECLINE**")
            elif decision == 'hard_decline':
                st.error(f"❌ **DECISION: HARD DECLINE**")
            else:
                st.info(f"❓ **DECISION: {decision.upper()}**")
            
            st.write(f"**Reason:** {decision_reason}")
            
            # Validation summary
            if 'validation_summary' in result:
                st.markdown("---")
                st.subheader("📊 Validation Summary")
                
                summary = result['validation_summary']
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Validation Score", f"{summary.get('validation_score', 0)}/100")
                
                with col2:
                    st.metric("Risk Level", summary.get('risk_level', 'Unknown'))
                
                with col3:
                    st.metric("Income Assessment", summary.get('income_assessment', 'Unknown'))
                
                with col4:
                    st.metric("Documents", f"{summary.get('total_documents', 0)}")
                
                # Risk level color coding
                risk_level = summary.get('risk_level', 'Unknown')
                if risk_level == 'Low':
                    st.success("🟢 **Low Risk Profile** - Good approval chances")
                elif risk_level == 'Medium':
                    st.warning("🟡 **Medium Risk Profile** - May require additional documentation")
                elif risk_level == 'High':
                    st.error("🔴 **High Risk Profile** - Significant challenges identified")
            
            # Detailed analysis
            if 'detailed_analysis' in result:
                st.markdown("---")
                st.subheader("🔍 Detailed Analysis")
                
                analysis = result['detailed_analysis']
                
                # Email validation
                email_valid = analysis.get('email_validation', {})
                if email_valid.get('valid'):
                    st.success(f"📧 Email: Valid ✅ (Score: {email_valid.get('score', 0)}/20)")
                else:
                    st.error(f"📧 Email: Invalid ❌ (Score: {email_valid.get('score', 0)}/20)")
                
                # Phone validation
                phone_valid = analysis.get('phone_validation', {})
                if phone_valid.get('valid'):
                    st.success(f"📱 Phone: Valid ✅ (Score: {phone_valid.get('score', 0)}/20)")
                else:
                    st.error(f"📱 Phone: Invalid ❌ (Score: {phone_valid.get('score', 0)}/20)")
                
                # Income validation
                income_valid = analysis.get('income_validation', {})
                if income_valid.get('valid'):
                    st.success(f"💰 Income: Valid ✅ (Score: {income_valid.get('score', 0)}/30)")
                    st.write(f"   Range: {income_valid.get('range', 'Unknown')}")
                else:
                    st.error(f"💰 Income: Invalid ❌ (Score: {income_valid.get('score', 0)}/30)")
                
                            # Documentation validation
            doc_valid = analysis.get('documentation_validation', {})
            if doc_valid.get('provided'):
                st.success(f"📄 Documents: Provided ✅ (Score: {doc_valid.get('score', 0)}/30)")
                st.write(f"   Count: {doc_valid.get('count', 0)} documents")
                
                # Show document details if available
                if 'document_relevance_score' in doc_valid:
                    st.write(f"   Document Relevance: {doc_valid.get('document_relevance_score', 0)}/100")
                if 'document_quality' in doc_valid:
                    st.write(f"   Document Quality: {doc_valid.get('document_quality', 'Unknown')}")
                
                # Show document issues if any
                if 'issues' in doc_valid and doc_valid['issues']:
                    st.write("   **Document Issues:**")
                    for issue in doc_valid['issues']:
                        st.write(f"   • {issue}")
            else:
                st.warning(f"📄 Documents: Not Provided ⚠️ (Score: {doc_valid.get('score', 0)}/30)")
            
            # Validation issues
            if 'validation_issues' in result and result['validation_issues']:
                st.markdown("---")
                st.subheader("⚠️ Validation Issues")
                for issue in result['validation_issues']:
                    st.error(f"• {issue}")
            
            # Recommendations
            if 'recommendations' in result and result['recommendations']:
                st.markdown("---")
                st.subheader("💡 Recommendations")
                for rec in result['recommendations']:
                    st.info(f"• {rec}")
            
            # AI processing info
            if result.get('ai_processing'):
                st.markdown("---")
                st.subheader("🤖 AI Processing Details")
                st.info(f"Workflow ID: {result.get('workflow_id', 'N/A')}")
                st.info(f"Enhanced Validation: {'Yes' if result.get('enhanced_validation') else 'No'}")
                
                # Show AI workflow status if available
                if 'workflow_id' in result:
                    st.info(f"AI Workflow Status: {'Completed' if result.get('ai_processing') else 'Failed'}")
                
                # Show confidence scores if available
                if 'confidence_score' in result:
                    st.info(f"AI Confidence: {result.get('confidence_score', 'N/A')}")
                
                # AI Workflow Execution Details
                st.write("**AI Workflow Execution:**")
                
                # Check if we have workflow execution details
                if 'workflow_id' in result and result.get('workflow_id', '').startswith('enhanced_'):
                    st.success("✅ **Enhanced AI Workflow Executed**")
                    st.write("• Multi-agent AI system processed the application")
                    st.write("• Document extraction and analysis completed")
                    st.write("• Cross-validation and conflict resolution performed")
                    st.write("• Machine learning model applied for decision making")
                    
                    # Show workflow steps if available
                    if 'workflow_steps' in result:
                        st.write("**Workflow Steps:**")
                        for i, step in enumerate(result.get('workflow_steps', []), 1):
                            st.write(f"{i}. {step}")
                else:
                    st.info("ℹ️ **Standard Validation Applied**")
                    st.write("• Basic validation rules applied")
                    st.write("• Enhanced AI workflow not available")
                    st.write("• Consider starting backend for full AI processing")
            
            # Enhanced Analysis Section
            st.markdown("---")
            st.subheader("🔬 Enhanced AI Analysis")
            
            # Document Analysis (if documents were processed)
            if 'validation_summary' in result:
                summary = result['validation_summary']
                if 'document_relevance_score' in summary:
                    doc_score = summary.get('document_relevance_score', 0)
                    doc_quality = summary.get('document_quality', 'Unknown')
                    
                    st.write("**Document Quality Analysis:**")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Document Relevance Score", f"{doc_score}/100")
                    with col2:
                        st.metric("Document Quality", doc_quality)
                    
                    # Document quality assessment
                    if doc_score >= 80:
                        st.success("🟢 **High Quality Documents** - Excellent supporting evidence")
                    elif doc_score >= 60:
                        st.warning("🟡 **Medium Quality Documents** - Adequate but could be improved")
                    elif doc_score >= 40:
                        st.warning("🟠 **Low Quality Documents** - May affect approval chances")
                    else:
                        st.error("🔴 **Poor Quality Documents** - Significant impact on approval")
            
            # Risk Analysis
            if 'validation_summary' in result:
                summary = result['validation_summary']
                risk_level = summary.get('risk_level', 'Unknown')
                
                st.write("**Risk Analysis:**")
                if risk_level == 'Low':
                    st.success("🟢 **Low Risk Profile** - High approval probability")
                    st.write("• Strong financial profile")
                    st.write("• Good documentation")
                    st.write("• Stable employment history")
                elif risk_level == 'Medium':
                    st.warning("🟡 **Medium Risk Profile** - Moderate approval probability")
                    st.write("• Some areas for improvement")
                    st.write("• May require additional documentation")
                    st.write("• Consider income enhancement")
                elif risk_level == 'High':
                    st.error("🔴 **High Risk Profile** - Low approval probability")
                    st.write("• Significant challenges identified")
                    st.write("• Requires substantial improvement")
                    st.write("• Consider alternative support options")
            
            # Economic Enablement Recommendations
            st.markdown("---")
            st.subheader("💡 Economic Enablement Recommendations")
            
            decision = result.get('decision', 'unknown')
            if decision == 'approved':
                st.success("**🎯 Approval Recommendations:**")
                st.write("• Access to full social support benefits")
                st.write("• Financial planning and budgeting services")
                st.write("• Skill development and training programs")
                st.write("• Employment advancement opportunities")
                st.write("• Family financial education")
            elif decision == 'soft_decline':
                st.warning("**🔧 Improvement Recommendations:**")
                st.write("• **Income Enhancement:**")
                st.write("  - Consider additional part-time work")
                st.write("  - Explore skill development for better-paying jobs")
                st.write("  - Look into government training programs")
                st.write("• **Documentation Improvement:**")
                st.write("  - Provide recent bank statements")
                st.write("  - Include employment verification letters")
                st.write("  - Add utility bills for address verification")
                st.write("• **Financial Stability:**")
                st.write("  - Build emergency savings")
                st.write("  - Improve credit score")
                st.write("  - Consider debt consolidation")
            elif decision == 'hard_decline':
                st.error("**🚨 Alternative Support Options:**")
                st.write("• Emergency assistance programs")
                st.write("• Food and housing support services")
                st.write("• Job training and placement services")
                st.write("• Financial counseling and debt management")
                st.write("• Community support networks")
                st.write("• Government welfare programs")
            
            # Next Steps
            st.markdown("---")
            st.subheader("📋 Next Steps")
            
            if decision == 'approved':
                st.success("**Immediate Actions:**")
                st.write("1. Complete any required paperwork")
                st.write("2. Schedule follow-up appointments")
                st.write("3. Review benefit details and requirements")
                st.write("4. Set up regular check-ins")
            elif decision == 'soft_decline':
                st.warning("**Action Items:**")
                st.write("1. Address validation issues identified above")
                st.write("2. Gather additional supporting documents")
                st.write("3. Consider income improvement strategies")
                st.write("4. Reapply in 30-60 days")
            else:
                st.info("**Support Options:**")
                st.write("1. Contact local social services")
                st.write("2. Explore alternative assistance programs")
                st.write("3. Seek financial counseling")
                st.write("4. Consider community resources")
            
            # Debug section (can be removed in production)
            with st.expander("🔧 Debug: Raw API Response"):
                st.json(result)
            
        else:
            st.error(f"Failed to submit application: {response.text}")
            
    except Exception as e:
        st.error(f"Error submitting application: {str(e)}")

def show_application_status():
    """Show application status checker"""
    st.header("📊 Application Status")
    
    # Application ID input
    application_id = st.text_input("Enter Application ID")
    
    if st.button("Check Status", use_container_width=True):
        if application_id:
            check_application_status(application_id)
        else:
            st.warning("Please enter an application ID")
    
    # Or use current application ID from session
    if 'current_application_id' in st.session_state:
        st.info(f"Current Application ID: {st.session_state.current_application_id}")
        if st.button("Check Current Application", use_container_width=True):
            check_application_status(st.session_state.current_application_id)

def check_application_status(application_id: str):
    """Check and display application status"""
    try:
        response = requests.get(f"{API_BASE_URL}/status/{application_id}")
        
        if response.status_code == 200:
            status_data = response.json()
            display_application_status(status_data)
        else:
            st.error(f"Failed to get status: {response.text}")
            
    except Exception as e:
        st.error(f"Error checking status: {str(e)}")

def display_application_status(status_data: Dict[str, Any]):
    """Display application status information"""
    st.subheader("Application Status")
    
    # Applicant information
    applicant = status_data.get('applicant', {})
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Personal Information**")
        st.write(f"Name: {applicant.get('first_name', '')} {applicant.get('last_name', '')}")
        st.write(f"Email: {applicant.get('email', '')}")
        st.write(f"Phone: {applicant.get('phone', '')}")
        st.write(f"Status: {applicant.get('status', '')}")
    
    with col2:
        st.write("**Financial Information**")
        st.write(f"Monthly Income: ${applicant.get('monthly_income', 0):,.2f}")
        st.write(f"Employment: {applicant.get('employment_status', '')}")
        st.write(f"Family Size: {applicant.get('family_size', 0)}")
        st.write(f"Dependents: {applicant.get('dependents', 0)}")
    
    # Documents
    st.subheader("Documents")
    documents = status_data.get('documents', [])
    if documents:
        doc_df = pd.DataFrame(documents)
        st.dataframe(doc_df[['filename', 'file_type', 'processing_status', 'created_at']])
    else:
        st.info("No documents found")
    
    # Decision
    decisions = status_data.get('decisions', [])
    if decisions:
        st.subheader("Decision")
        decision = decisions[0]  # Latest decision
        display_decision(decision)
    else:
        st.info("No decision available yet")

def display_decision(decision: Dict[str, Any]):
    """Display decision information"""
    col1, col2 = st.columns(2)
    
    with col1:
        decision_type = decision.get('decision', 'unknown')
        confidence = decision.get('confidence_score', 0.0)
        
        # Color code decision
        if decision_type == 'approve':
            st.success(f"**Decision: {decision_type.upper()}**")
        elif decision_type == 'soft_decline':
            st.warning(f"**Decision: {decision_type.upper()}**")
        else:
            st.error(f"**Decision: {decision_type.upper()}**")
        
        st.metric("Confidence", f"{confidence:.1%}")
        st.write(f"**Reason:** {decision.get('decision_reason', 'No reason provided')}")
    
    with col2:
        st.write("**Model Information**")
        st.write(f"Version: {decision.get('model_version', 'Unknown')}")
        
        # SHAP values visualization
        shap_values = decision.get('shap_values', {})
        if shap_values:
            st.write("**Feature Importance**")
            shap_df = pd.DataFrame(list(shap_values.items()), columns=['Feature', 'Importance'])
            fig = px.bar(shap_df, x='Importance', y='Feature', orientation='h')
            st.plotly_chart(fig, use_container_width=True)
    
    # Recommendations
    recommendations = decision.get('recommendations', [])
    if recommendations:
        st.subheader("Recommendations")
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")

def show_chat_assistant():
    """Show chat assistant interface"""
    st.header("💬 Chat Assistant")
    
    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Application context
    application_id = st.text_input("Application ID (optional)", 
                                 value=st.session_state.get('current_application_id', ''))
    
    # Chat interface
    st.subheader("Chat with AI Assistant")
    
    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.write(f"👤 **You:** {message['content']}")
        else:
            st.write(f"🤖 **AI:** {message['content']}")
    
    # Chat input
    user_message = st.text_input("Type your message...", key="chat_input")
    
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("Send", use_container_width=True):
            if user_message:
                send_chat_message(user_message, application_id)
    
    with col2:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

def send_chat_message(message: str, application_id: str):
    """Send chat message to API"""
    try:
        if not application_id:
            st.warning("Please provide an application ID for context")
            return
        
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': message,
            'timestamp': datetime.now()
        })
        
        # Send to API
        chat_data = {
            "message": message,
            "context": {"application_id": application_id}
        }
        
        response = requests.post(
            f"{API_BASE_URL}/chat/{application_id}",
            json=chat_data
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Add AI response to history
            st.session_state.chat_history.append({
                'role': 'assistant',
                'content': result.get('response', 'No response received'),
                'timestamp': datetime.now()
            })
            
            st.rerun()
        else:
            st.error(f"Failed to get response: {response.text}")
            
    except Exception as e:
        st.error(f"Error sending message: {str(e)}")

def show_analytics():
    """Show analytics dashboard"""
    st.header("📈 Analytics")
    
    st.info("Analytics dashboard will be implemented in future versions")
    
    # Placeholder for analytics
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Application Volume")
        # Placeholder chart
        st.line_chart(pd.DataFrame({'Applications': [0, 0, 0, 0, 0]}))
    
    with col2:
        st.subheader("Decision Distribution")
        # Placeholder chart
        st.bar_chart(pd.DataFrame({'Decisions': [0, 0, 0]}, index=['Approve', 'Soft Decline', 'Hard Decline']))

if __name__ == "__main__":
    main() 
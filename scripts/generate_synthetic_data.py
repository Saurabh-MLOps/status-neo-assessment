#!/usr/bin/env python3
"""
Synthetic data generator for Social Support AI System
"""

import os
import sys
import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

# Add parent directory to path to import app modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import get_db, init_db
from app.models.database_models import Applicant, Document, ExtractedData, Decision

# Indian names data
INDIAN_FIRST_NAMES = [
    "Aarav", "Arjun", "Advait", "Dhruv", "Ishaan", "Krishna", "Neel", "Rohan", "Shaan", "Vivaan",
    "Aanya", "Diya", "Ira", "Kiara", "Mira", "Nisha", "Priya", "Riya", "Sana", "Zara",
    "Aditya", "Aryan", "Dev", "Harsh", "Kabir", "Lakshay", "Om", "Rudra", "Shiv", "Ved",
    "Ananya", "Avni", "Gauri", "Jiya", "Kavya", "Myra", "Pari", "Sia", "Tara", "Yashvi"
]

INDIAN_LAST_NAMES = [
    "Patel", "Singh", "Kumar", "Sharma", "Verma", "Gupta", "Malhotra", "Kapoor", "Joshi", "Chopra",
    "Reddy", "Iyer", "Menon", "Nair", "Pillai", "Krishnan", "Rao", "Naidu", "Gowda", "Shetty",
    "Mehta", "Desai", "Shah", "Bhatt", "Pandey", "Yadav", "Jha", "Tiwari", "Mishra", "Dubey"
]

INDIAN_CITIES = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Chennai", "Kolkata", "Pune", "Ahmedabad", "Jaipur", "Surat",
    "Lucknow", "Kanpur", "Nagpur", "Indore", "Thane", "Bhopal", "Visakhapatnam", "Pimpri-Chinchwad", "Patna", "Vadodara",
    "Ghaziabad", "Ludhiana", "Agra", "Nashik", "Faridabad", "Meerut", "Rajkot", "Kalyan-Dombivali", "Vasai-Virar", "Varanasi"
]

INDIAN_STATES = [
    "Maharashtra", "Delhi", "Karnataka", "Telangana", "Tamil Nadu", "West Bengal", "Gujarat", "Rajasthan", "Uttar Pradesh", "Madhya Pradesh",
    "Andhra Pradesh", "Bihar", "Punjab", "Haryana", "Jharkhand", "Odisha", "Assam", "Chhattisgarh", "Kerala", "Uttarakhand"
]

INDIAN_EMPLOYERS = [
    "Tata Consultancy Services", "Infosys", "Wipro", "HCL Technologies", "Tech Mahindra", "Larsen & Toubro", "Reliance Industries",
    "Bharti Airtel", "HDFC Bank", "ICICI Bank", "State Bank of India", "Axis Bank", "Kotak Mahindra Bank", "Hindustan Unilever",
    "ITC Limited", "Maruti Suzuki", "Tata Motors", "Mahindra & Mahindra", "Hero MotoCorp", "Bajaj Auto"
]

INDIAN_EMPLOYMENT_STATUSES = [
    "Full-time", "Part-time", "Contract", "Freelance", "Self-employed", "Unemployed", "Student", "Retired"
]

def generate_synthetic_applicants(n_applicants: int = 100) -> list:
    """Generate synthetic Indian applicants"""
    applicants = []
    
    for i in range(n_applicants):
        # Generate realistic Indian data
        first_name = random.choice(INDIAN_FIRST_NAMES)
        last_name = random.choice(INDIAN_LAST_NAMES)
        
        # Generate realistic Indian income (in INR)
        base_income = random.choice([15000, 25000, 35000, 45000, 55000, 75000, 95000, 120000, 150000, 200000])
        income_variation = random.uniform(0.8, 1.2)
        monthly_income = round(base_income * income_variation, 2)
        
        # Generate realistic Indian employment data
        employment_status = random.choice(INDIAN_EMPLOYMENT_STATUSES)
        if employment_status in ["Full-time", "Part-time", "Contract"]:
            employer_name = random.choice(INDIAN_EMPLOYERS)
            employment_length_months = random.randint(1, 120)
        elif employment_status == "Self-employed":
            employer_name = f"{first_name} {last_name} Enterprises"
            employment_length_months = random.randint(6, 60)
        else:
            employer_name = None
            employment_length_months = 0
        
        # Generate realistic Indian family data
        family_size = random.randint(2, 8)  # Indian families tend to be larger
        dependents = random.randint(0, min(4, family_size - 2))
        
        # Generate realistic Indian address
        city = random.choice(INDIAN_CITIES)
        state = random.choice(INDIAN_STATES)
        
        # Generate realistic Indian phone number
        phone = f"+91 {random.randint(7000000000, 9999999999)}"
        
        # Generate realistic Indian email
        email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com'])}"
        
        applicant = {
            "first_name": first_name,
            "last_name": last_name,
            "date_of_birth": (datetime.now() - timedelta(days=random.randint(6570, 21900))).strftime("%Y-%m-%d"),  # 18-60 years
            "email": email,
            "phone": phone,
            "street_address": f"{random.randint(1, 999)} {random.choice(['Street', 'Road', 'Lane', 'Avenue', 'Colony', 'Nagar'])}, {random.choice(['Sector', 'Area', 'Block'])} {random.randint(1, 20)}",
            "city": city,
            "state": state,
            "postal_code": str(random.randint(100000, 999999)),
            "country": "India",
            "monthly_income": monthly_income,
            "employment_status": employment_status,
            "employer_name": employer_name,
            "employment_length_months": employment_length_months,
            "family_size": family_size,
            "dependents": dependents,
            "status": "pending",
            "created_at": datetime.now() - timedelta(days=random.randint(0, 30))
        }
        applicants.append(applicant)
    
    return applicants

def generate_synthetic_documents(applicant_id: str) -> list:
    """Generate synthetic documents for Indian applicants"""
    document_types = ["government_id", "bank_statement", "pay_stub", "utility_bill", "rental_agreement"]
    documents = []
    
    for doc_type in random.sample(document_types, random.randint(2, 4)):
        document = {
            "applicant_id": applicant_id,
            "filename": f"{doc_type}_{applicant_id[:8]}.pdf",
            "document_type": doc_type,
            "upload_date": datetime.now() - timedelta(days=random.randint(0, 7)),
            "file_size": random.randint(50000, 500000),
            "status": "uploaded"
        }
        documents.append(document)
    
    return documents

def generate_synthetic_extracted_data(applicant_id: str, document_id: str) -> list:
    """Generate synthetic extracted data with Indian context"""
    extracted_data = {
        "document_id": document_id,
        "applicant_id": applicant_id,
        "extraction_method": random.choice(["ocr", "pdf_parser", "table_extractor", "text_parser"]),
        "confidence_score": round(random.uniform(0.7, 0.98), 2),
        "extracted_text": f"Sample extracted text from Indian document {document_id}",
        "structured_data": {
            "name": f"{random.choice(INDIAN_FIRST_NAMES)} {random.choice(INDIAN_LAST_NAMES)}",
            "address": f"{random.randint(1, 999)} {random.choice(INDIAN_CITIES)}",
            "income": f"₹{random.randint(15000, 200000):,}",
            "employment": random.choice(INDIAN_EMPLOYMENT_STATUSES)
        },
        "extraction_timestamp": datetime.now() - timedelta(hours=random.randint(1, 24)),
        "processing_time_ms": random.randint(100, 2000)
    }
    
    return [extracted_data]

def generate_synthetic_decisions(applicant_id: str) -> list:
    """Generate synthetic decisions with Indian context"""
    decisions = ["approve", "soft_decline", "hard_decline"]
    decision = random.choices(decisions, weights=[0.4, 0.4, 0.2])[0]
    
    # Generate realistic Indian context reasons
    indian_reasons = {
        "approve": [
            "Strong employment history with established Indian company",
            "Good credit score and stable income in INR",
            "Family size appropriate for income level",
            "Long-term employment in Indian market"
        ],
        "soft_decline": [
            "Income slightly below threshold for Indian cost of living",
            "Recent employment change in competitive Indian market",
            "Family size large relative to income",
            "Limited credit history in Indian banking system"
        ],
        "hard_decline": [
            "Insufficient income for Indian family size",
            "Unemployment in competitive Indian job market",
            "No established credit history in India",
            "Income below minimum wage requirements"
        ]
    }
    
    decision_data = {
        "applicant_id": applicant_id,
        "decision": decision,
        "confidence_score": round(random.uniform(0.6, 0.95), 2),
        "reason": random.choice(indian_reasons[decision]),
        "features_used": ["monthly_income", "employment_length_months", "family_size", "dependents"],
        "shap_values": {
            "monthly_income": round(random.uniform(0.1, 0.4), 3),
            "employment_length_months": round(random.uniform(0.05, 0.25), 3),
            "family_size": round(random.uniform(0.02, 0.15), 3),
            "dependents": round(random.uniform(0.01, 0.1), 3)
        },
        "recommendations": [
            "Consider Indian government social support programs",
            "Explore employment opportunities in Indian tech sector",
            "Build credit history through Indian banking products",
            "Consider family planning for better financial stability"
        ],
        "decision_timestamp": datetime.now() - timedelta(hours=random.randint(1, 12)),
        "model_version": "1.0.0"
    }
    
    return [decision_data]

def insert_synthetic_data(applicants: list):
    """Insert synthetic Indian data into database"""
    init_db()
    db = next(get_db())
    
    try:
        for i, applicant_data in enumerate(applicants):
            # Create applicant
            applicant = Applicant(**applicant_data)
            db.add(applicant)
            db.commit()
            db.refresh(applicant)
            
            # Generate documents
            documents = generate_synthetic_documents(applicant.id)
            for doc_data in documents:
                document = Document(**doc_data)
                db.add(document)
                db.commit()
                db.refresh(document)
                
                # Generate extracted data
                extracted_data_list = generate_synthetic_extracted_data(applicant.id, document.id)
                for ext_data in extracted_data_list:
                    extracted_data = ExtractedData(**ext_data)
                    db.add(extracted_data)
                
                # Generate decisions
                decisions = generate_synthetic_decisions(applicant.id)
                for decision_data in decisions:
                    decision = Decision(**decision_data)
                    db.add(decision)
            
            if (i + 1) % 10 == 0:
                print(f"✅ Processed {i + 1}/{len(applicants)} Indian applicants")
        
        db.commit()
        print(f"🎉 Successfully inserted {len(applicants)} Indian applicants with documents and decisions!")
        
    except Exception as e:
        print(f"❌ Error inserting data: {e}")
        db.rollback()
    finally:
        db.close()

def main():
    """Main function to generate and insert Indian synthetic data"""
    print("🇮🇳 Generating Indian Synthetic Data for Social Support AI System")
    print("=" * 70)
    
    # Generate Indian applicants
    n_applicants = int(input("Enter number of Indian applicants to generate (default 50): ") or "50")
    
    print(f"\n🎲 Generating {n_applicants} Indian applicants...")
    applicants = generate_synthetic_applicants(n_applicants)
    
    print(f"✅ Generated {len(applicants)} Indian applicants")
    
    # Show sample data
    if applicants:
        print(f"\n📊 Sample Indian Applicant:")
        sample = applicants[0]
        print(f"   Name: {sample['first_name']} {sample['last_name']}")
        print(f"   City: {sample['city']}, {sample['state']}")
        print(f"   Income: ₹{sample['monthly_income']:,.2f}")
        print(f"   Employment: {sample['employment_status']}")
        if sample['employer_name']:
            print(f"   Employer: {sample['employer_name']}")
        print(f"   Family Size: {sample['family_size']}")
        print(f"   Phone: {sample['phone']}")
        print(f"   Email: {sample['email']}")
    
    # Confirm insertion
    confirm = input(f"\n🚀 Insert {n_applicants} Indian applicants into database? (y/n): ").lower()
    if confirm in ['y', 'yes']:
        insert_synthetic_data(applicants)
    else:
        print("❌ Data generation cancelled")

if __name__ == "__main__":
    main() 
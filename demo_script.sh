#!/bin/bash
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
RESPONSE=$(curl -s -X POST "http://localhost:8000/ingest"   -H "Content-Type: application/json"   -d @- << 'EOF'
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
curl -s -X POST "http://localhost:8000/chat/$APP_ID"   -H "Content-Type: application/json"   -d '{"message": "What is the decision on my application?"}' | jq '.response'
echo

echo "✅ Demo completed successfully!"
echo "🌐 Frontend available at: http://localhost:8501"
echo "🔧 Backend API at: http://localhost:8000"

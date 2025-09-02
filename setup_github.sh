#!/bin/bash

echo "🚀 Setting up GitHub for Social Support AI System"
echo "=================================================="
echo

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized. Please run:"
    echo "   git init"
    echo "   git add ."
    echo "   git commit -m 'Initial commit'"
    exit 1
fi

echo "✅ Git repository is initialized"
echo

# Get current git status
echo "📊 Current Git Status:"
git status --short
echo

echo "🔧 To set up GitHub, follow these steps:"
echo
echo "1. 🆕 Go to https://github.com/new"
echo "2. 📝 Repository name: social-support-ai-system"
echo "3. 📝 Description: AI-powered social support application evaluation system"
echo "4. 🔒 Make it Public or Private (your choice)"
echo "5. ❌ DON'T initialize with README (we already have one)"
echo "6. ✅ Click 'Create repository'"
echo
echo "7. 🔗 Copy the repository URL from GitHub"
echo "8. 🚀 Run this command (replace YOUR_USERNAME with your GitHub username):"
echo "   git remote add origin https://github.com/YOUR_USERNAME/social-support-ai-system.git"
echo
echo "9. 📤 Push to GitHub:"
echo "   git push -u origin main"
echo

echo "💡 Quick Commands:"
echo "   # Add remote (replace YOUR_USERNAME)"
echo "   git remote add origin https://github.com/YOUR_USERNAME/social-support-ai-system.git"
echo "   "
echo "   # Push to GitHub"
echo "   git push -u origin main"
echo "   "
echo "   # Check remote"
echo "   git remote -v"
echo

echo "🎬 To create demo GIFs after pushing to GitHub:"
echo "   python3 scripts/create_demo_gifs.py"
echo

echo "🌐 Your applications are running at:"
echo "   • Frontend: http://localhost:8501"
echo "   • Backend: http://localhost:8000"
echo "   • API Docs: http://localhost:8000/docs" 
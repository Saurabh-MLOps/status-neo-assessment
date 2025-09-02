#!/usr/bin/env python3
"""
GitHub Setup Helper for Social Support AI System
This script helps you set up and push your code to GitHub.
"""

import os
import subprocess
import sys

def print_header():
    """Print a beautiful header"""
    print("🚀" + "="*60 + "🚀")
    print("🐙 GitHub Setup Helper - Social Support AI System 🐙")
    print("🚀" + "="*60 + "🚀")
    print()

def check_git_status():
    """Check current git status"""
    print("🔍 Checking Git Status...")
    
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git repository initialized")
            # Fix the f-string syntax issue
            status_output = result.stdout
            if 'On branch ' in status_output:
                branch_line = status_output.split('On branch ')[1]
                current_branch = branch_line.split('\n')[0]
                print(f"📝 Current branch: {current_branch}")
            return True
        else:
            print("❌ Git repository not initialized")
            return False
    except FileNotFoundError:
        print("❌ Git not found. Please install Git first.")
        return False

def check_remote():
    """Check if remote origin is configured"""
    print("\n🌐 Checking Remote Configuration...")
    
    try:
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if result.returncode == 0 and 'origin' in result.stdout:
            print("✅ Remote origin configured")
            print(result.stdout.strip())
            return True
        else:
            print("❌ No remote origin configured")
            return False
    except Exception as e:
        print(f"❌ Error checking remote: {e}")
        return False

def show_github_instructions():
    """Show step-by-step GitHub setup instructions"""
    print("\n📋 GitHub Setup Instructions")
    print("=" * 50)
    
    print("1. 🆕 Create a new repository on GitHub:")
    print("   • Go to https://github.com/new")
    print("   • Repository name: social-support-ai-system")
    print("   • Description: AI-powered social support application evaluation system")
    print("   • Make it Public or Private (your choice)")
    print("   • Don't initialize with README (we already have one)")
    print("   • Click 'Create repository'")
    
    print("\n2. 🔗 Add remote origin:")
    print("   • Copy the repository URL from GitHub")
    print("   • Run this command (replace YOUR_USERNAME):")
    print("     git remote add origin https://github.com/YOUR_USERNAME/social-support-ai-system.git")
    
    print("\n3. 🚀 Push to GitHub:")
    print("   git push -u origin main")
    
    print("\n4. 📝 Update README badges:")
    print("   • Replace 'yourusername' with your actual GitHub username in README.md")
    print("   • Update the repository URL in the clone command")

def show_demo_instructions():
    """Show instructions for creating demo GIFs"""
    print("\n🎬 Demo GIF Creation Instructions")
    print("=" * 50)
    
    print("1. 🎥 Record your demos:")
    print("   • Run: python3 scripts/create_demo_gifs.py")
    print("   • Follow the generated guides")
    print("   • Use Loom (recommended) or other screen recording tools")
    
    print("\n2. 📱 Recommended demo content:")
    print("   • Dashboard overview (10-15 seconds)")
    print("   • Application submission (20-25 seconds)")
    print("   • Document processing (15-20 seconds)")
    print("   • ML decision display (20-25 seconds)")
    print("   • Chat interface (15-20 seconds)")
    
    print("\n3. 🔗 Add GIFs to README:")
    print("   • Upload GIFs to your repository")
    print("   • Add them to README.md under '## 🎬 Demo' section")

def show_quick_commands():
    """Show quick commands for GitHub setup"""
    print("\n⚡ Quick Commands")
    print("=" * 50)
    
    print("🔧 Setup Commands:")
    print("  git remote add origin https://github.com/YOUR_USERNAME/social-support-ai-system.git")
    print("  git push -u origin main")
    
    print("\n📝 Update Commands:")
    print("  git add .")
    print("  git commit -m 'Update: description of changes'")
    print("  git push")
    
    print("\n🎬 Demo Commands:")
    print("  python3 scripts/create_demo_gifs.py")
    print("  python3 scripts/quick_demo.py")
    print("  python3 scripts/simple_test.py")

def main():
    """Main function"""
    print_header()
    
    # Check git status
    git_ok = check_git_status()
    
    if not git_ok:
        print("\n❌ Please initialize git repository first:")
        print("   git init")
        print("   git add .")
        print("   git commit -m 'Initial commit'")
        return
    
    # Check remote
    remote_ok = check_remote()
    
    if not remote_ok:
        print("\n⚠️ Remote origin not configured.")
        print("Follow the setup instructions below.")
    
    # Show instructions
    show_github_instructions()
    
    if not remote_ok:
        show_demo_instructions()
        show_quick_commands()
    else:
        print("\n✅ Your repository is ready!")
        print("You can now push updates with:")
        print("  git push")
        
        print("\n🎬 To create demo GIFs:")
        print("  python3 scripts/create_demo_gifs.py")

if __name__ == "__main__":
    main() 
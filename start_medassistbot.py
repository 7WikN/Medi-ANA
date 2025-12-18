#!/usr/bin/env python3
"""
MedAssistBot Startup Script
Easily start the backend server and open the UI
"""

import subprocess
import webbrowser
import time
import os
import sys
from pathlib import Path

def check_requirements():
    """Check if all requirements are met"""
    print("🔍 Checking requirements...")
    
    # Check if we're in the right directory
    if not os.path.exists("Backend/app.py"):
        print("❌ Please run this script from the MedAssistBot root directory")
        return False
    
    # Check if virtual environment exists
    if not os.path.exists("Backend/venv") and not os.path.exists("Backend/.venv"):
        print("⚠️  Virtual environment not found. Please set up the backend first.")
        print("   Run: cd Backend && python -m venv venv && venv\\Scripts\\activate && pip install -r requirements.txt")
        return False
    
    # Check if .env file exists
    if not os.path.exists("Backend/.env"):
        print("⚠️  .env file not found. Please create Backend/.env with your GEMINI_API_KEY")
        return False
    
    print("✅ Requirements check passed")
    return True

def start_backend():
    """Start the FastAPI backend server"""
    print("\n🚀 Starting MedAssistBot Backend...")
    
    # Change to backend directory
    os.chdir("Backend")
    
    # Determine the correct python executable
    if os.path.exists("venv/Scripts/python.exe"):
        python_exe = "venv/Scripts/python.exe"
    elif os.path.exists(".venv/Scripts/python.exe"):
        python_exe = ".venv/Scripts/python.exe"
    else:
        python_exe = "python"
    
    # Start the server
    cmd = [python_exe, "-m", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if process is still running
        if process.poll() is None:
            print("✅ Backend server started successfully on http://localhost:8000")
            return process
        else:
            stdout, stderr = process.communicate()
            print(f"❌ Backend failed to start:")
            print(f"   stdout: {stdout}")
            print(f"   stderr: {stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        return None

def open_ui():
    """Open the UI in the default web browser"""
    print("\n🌐 Opening MedAssistBot UI...")
    
    # Go back to root directory
    os.chdir("..")
    
    # Get the absolute path to the UI files
    ui_path = Path("UI").absolute()
    
    # Open the main pages
    pages = [
        ("Landing Page", ui_path / "index.html"),
        ("Chat Interface", ui_path / "chat.html"),
        ("Dashboard", ui_path / "dashboard.html")
    ]
    
    print("\n📱 Available UI Pages:")
    for name, path in pages:
        print(f"   - {name}: file://{path}")
    
    # Open the chat interface by default
    chat_url = f"file://{ui_path / 'chat.html'}"
    try:
        webbrowser.open(chat_url)
        print(f"\n✅ Opened chat interface: {chat_url}")
    except Exception as e:
        print(f"⚠️  Could not auto-open browser: {e}")
        print(f"   Please manually open: {chat_url}")

def main():
    """Main startup function"""
    print("🏥 MedAssistBot Startup Script")
    print("=" * 40)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("\n❌ Failed to start backend. Please check the error messages above.")
        sys.exit(1)
    
    # Open UI
    open_ui()
    
    print("\n" + "=" * 40)
    print("🎉 MedAssistBot is now running!")
    print("=" * 40)
    print("📍 Backend API: http://localhost:8000")
    print("📍 API Docs: http://localhost:8000/docs")
    print("📍 Health Check: http://localhost:8000/health")
    print("\n💡 Tips:")
    print("   - Use the chat interface to test the AI")
    print("   - Check the dashboard for analytics")
    print("   - Press Ctrl+C to stop the backend")
    
    try:
        # Keep the script running
        print("\n⏳ Backend is running... Press Ctrl+C to stop")
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping MedAssistBot...")
        backend_process.terminate()
        backend_process.wait()
        print("✅ Backend stopped successfully")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

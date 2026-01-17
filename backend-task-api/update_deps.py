#!/usr/bin/env python3
"""
Script to install updated requirements and run the application
"""

import subprocess
import sys
import os

def install_requirements():
    """Install the updated requirements"""
    print("Installing updated requirements...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                              check=True, capture_output=True, text=True)
        print("Requirements installed successfully!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def main():
    # Change to the backend directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("Updating authentication endpoints for better performance...")
    install_requirements()
    print("\nSetup complete! You can now run the server with:")
    print("python run_server.py")

if __name__ == "__main__":
    main()
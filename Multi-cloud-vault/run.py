#!/usr/bin/env python3
"""
Check Python version compatibility and run the app
"""

import sys

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    print(f"🐍 Python Version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3:
        print("❌ Python 3 is required!")
        sys.exit(1)
    
    if version.minor >= 14:
        print("⚠️  WARNING: Python 3.14+ may have compatibility issues with secretsharing library")
        print("   Recommended: Use Python 3.9-3.13")
        print("   Attempting to run anyway...")
    
    return True

if __name__ == "__main__":
    check_python_version()
    
    # Try to import required modules
    try:
        import secretsharing
        import cryptography
        import boto3
        print("✅ All dependencies installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("\nPlease install dependencies:")
        print("  pip install secretsharing cryptography boto3 google-api-python-client")
        sys.exit(1)
    
    # Import and run the app
    try:
        from app import main
        print("\n🚀 Starting Multi-Cloud Vault...")
        main()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

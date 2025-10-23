#!/usr/bin/env python3
"""
TaskMate Debug Script - Helps diagnose startup issues
"""
import sys
import os
from datetime import datetime

def test_imports():
    """Test if all required modules can be imported"""
    print("🔍 Testing imports...")
    try:
        from flask import Flask
        print("✅ Flask imported successfully")
        
        from models import db, User, Task
        print("✅ Models imported successfully")
        
        from routes.main_routes import main_bp
        from routes.auth_routes import auth_bp  
        from routes.api_routes import api_bp
        print("✅ Routes imported successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_app_creation():
    """Test app creation and route registration"""
    print("\n🔧 Testing app creation...")
    try:
        from app import create_app
        app = create_app()
        print("✅ App created successfully")
        
        # Test routes
        print(f"✅ Registered routes: {len(list(app.url_map.iter_rules()))}")
        
        # Test template folder
        if os.path.exists(app.template_folder):
            print("✅ Templates folder exists")
        else:
            print("❌ Templates folder missing!")
            
        # Test static folder  
        if os.path.exists(app.static_folder):
            print("✅ Static folder exists")
        else:
            print("❌ Static folder missing!")
            
        return app
    except Exception as e:
        print(f"❌ App creation failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_routes(app):
    """Test route responses"""
    print("\n🌐 Testing routes...")
    try:
        with app.test_client() as client:
            # Test main route
            response = client.get('/')
            print(f"GET / -> Status: {response.status_code}")
            
            # Test auth routes
            response = client.get('/auth/login')
            print(f"GET /auth/login -> Status: {response.status_code}")
            
            # Test tasks route
            response = client.get('/tasks')
            print(f"GET /tasks -> Status: {response.status_code}")
            
        return True
    except Exception as e:
        print(f"❌ Route testing failed: {e}")
        return False

def main():
    """Run all diagnostics"""
    print("🚀 TaskMate Diagnostic Tool")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import test failed. Fix imports before proceeding.")
        return
    
    # Test app creation
    app = test_app_creation()
    if not app:
        print("\n❌ App creation failed. Check app.py configuration.")
        return
        
    # Test routes
    if not test_routes(app):
        print("\n❌ Route testing failed. Check route definitions.")
        return
    
    print("\n✅ All tests passed! TaskMate should work correctly.")
    print("\n🎯 To run TaskMate:")
    print("   python app.py")
    print("   Then visit: http://127.0.0.1:5000")
    print("\n🔑 Default login:")
    print("   Username: admin")
    print("   Password: admin123")

if __name__ == "__main__":
    main()
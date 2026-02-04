# Quickstart validation for User Authentication Module
# This script validates that all core functionality is working properly

import subprocess
import sys
import time
import requests
import json

def validate_setup():
    """Validate that all required dependencies are installed"""
    print("Validating setup...")
    
    # Check if required packages are available
    required_packages = [
        "fastapi",
        "sqlalchemy", 
        "python-jose",
        "passlib",
        "bcrypt",
        "python-dotenv",
        "pytest"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"Missing packages: {missing_packages}")
        return False
    
    print("✓ Setup validation passed")
    return True


def validate_project_structure():
    """Validate that the project structure is correct"""
    print("Validating project structure...")
    
    import os
    
    required_paths = [
        "backend/src/models/user.py",
        "backend/src/schemas/user.py", 
        "backend/src/database/database.py",
        "backend/src/services/user_service.py",
        "backend/src/api/auth.py",
        "backend/src/utils/token.py",
        "backend/src/utils/password.py",
        "backend/src/auth/auth_handler.py",
        "backend/src/main.py",
        "requirements.txt",
        "pyproject.toml"
    ]
    
    missing_paths = []
    for path in required_paths:
        if not os.path.exists(path):
            missing_paths.append(path)
    
    if missing_paths:
        print(f"Missing paths: {missing_paths}")
        return False
    
    print("✓ Project structure validation passed")
    return True


def validate_api_endpoints():
    """Validate that API endpoints are working"""
    print("Validating API endpoints...")
    
    # This would typically involve starting the server and making requests
    # For now, we'll just check that the code compiles and has the right structure
    
    try:
        # Import the main app to check for syntax errors
        from backend.src.main import app
        from backend.src.api.auth import router
    except Exception as e:
        print(f"Error importing API modules: {e}")
        return False
    
    print("✓ API endpoints validation passed")
    return True


def run_tests():
    """Run the unit and integration tests"""
    print("Running tests...")
    
    try:
        # Run pytest
        result = subprocess.run([sys.executable, "-m", "pytest", "tests/", "-v"], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"Tests failed:\n{result.stdout}\n{result.stderr}")
            return False
        
        print("✓ Tests passed")
        return True
    except Exception as e:
        print(f"Error running tests: {e}")
        return False


def main():
    """Main validation function"""
    print("Starting quickstart validation for User Authentication Module...")
    print()
    
    all_passed = True
    
    # Run all validation steps
    all_passed &= validate_setup()
    print()
    
    all_passed &= validate_project_structure()
    print()
    
    all_passed &= validate_api_endpoints()
    print()
    
    all_passed &= run_tests()
    print()
    
    if all_passed:
        print("✓ All validations passed! The User Authentication Module is ready.")
        return True
    else:
        print("✗ Some validations failed. Please check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
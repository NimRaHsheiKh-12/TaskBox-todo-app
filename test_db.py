import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'backend'))

from src.database.database import check_db_connection, create_db_and_tables
from src.config import settings

print(f"Database URL: {settings.database_url}")

print("Testing database connection...")
try:
    result = check_db_connection()
    print(f"Database connection result: {result}")
except Exception as e:
    print(f"Database connection failed: {e}")
    import traceback
    traceback.print_exc()

print("Testing model creation...")
try:
    # This will test if the models can be properly created
    create_db_and_tables()
    print("Models created successfully")
except Exception as e:
    print(f"Model creation failed: {e}")
    import traceback
    traceback.print_exc()
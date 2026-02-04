"""
Vercel serverless function handler for the FastAPI backend
"""
from mangum import Mangum
import sys
import os

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.src.main import app

# Create the ASGI handler for Vercel
handler = Mangum(app, lifespan="off")

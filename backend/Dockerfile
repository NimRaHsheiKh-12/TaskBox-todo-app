HEAD
# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy project requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "backend.src.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install OS dependencies (optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install dependencies
COPY requirements.txt .
RUN python -m pip install --upgrade pip
RUN python -m pip install --no-cache-dir -r requirements.txt

# Copy backend source code (all inside src)
COPY ./app ./src

 HEAD
# Copy project (backend only)
COPY ./src ./src
COPY ./api ./api

# Expose Hugging Face default port
EXPOSE 7860

# Run the FastAPI application

# Expose Hugging Face port
EXPOSE 7860

# Start FastAPI using uvicorn
 853fc96 (Initial FastAPI Docker deployment)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]
 003-chatbot-taskbox

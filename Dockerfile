# Use official Python image as a base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies 
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    postgresql-client

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Add entrypoint.sh and make it executable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh

# Use shell form to run entrypoint.sh
ENTRYPOINT ["/bin/bash", "/app/entrypoint.sh"]

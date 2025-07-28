# Use slim base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Install required system dependencies for PyMuPDF and font rendering
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libglib2.0-0 \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY src/main.py .

# Ensure input/output folders exist inside the container
RUN mkdir -p /app/input /app/output

# Run the application
CMD ["python", "main.py"]

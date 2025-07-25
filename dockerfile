# -----------------------------------------------
# Use official lightweight Python base image
# -----------------------------------------------
FROM python:3.10-slim

# -----------------------------------------------
# Install system dependencies
# -----------------------------------------------
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------
# Set working directory
# -----------------------------------------------
WORKDIR /app

# -----------------------------------------------
# Copy dependency list first (for layer caching)
# -----------------------------------------------
COPY requirements.txt .

# -----------------------------------------------
# Install Python dependencies
# -----------------------------------------------
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------
# Copy the rest of the project files
# -----------------------------------------------
COPY . .

# -----------------------------------------------
# Pre-download MiniLM weights so you don’t need internet at runtime
# -----------------------------------------------
RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# -----------------------------------------------
# Define default command
# -----------------------------------------------
CMD ["python", "main.py"]

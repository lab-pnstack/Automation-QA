FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create directories
RUN mkdir -p reports screenshots

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV BROWSER=chrome
ENV HEADLESS=true

# Run tests
CMD ["pytest", "tests/", "-v", "-n", "auto"]

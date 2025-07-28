# Use Python 3.11 slim image for smaller size
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY pyproject.toml uv.lock ./

# Install UV package manager
RUN pip install uv

# Install Python dependencies
RUN uv sync --frozen

# Copy application files
COPY . .

# Create .streamlit directory and config
RUN mkdir -p .streamlit
COPY .streamlit/config.toml .streamlit/

# Expose port 5000
EXPOSE 5000

# Health check
HEALTHCHECK CMD curl --fail http://localhost:5000/_stcore/health

# Run the application
CMD ["uv", "run", "streamlit", "run", "app.py", "--server.port=5000", "--server.address=0.0.0.0"]
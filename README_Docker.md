# Intelligent Document Analyst - Docker Setup

This guide explains how to run the Intelligent Document Analyst locally using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (usually included with Docker Desktop)

## Quick Start

### Option 1: Using Docker Compose (Recommended)

1. Clone or download the project files
2. Navigate to the project directory
3. Run the application:

```bash
docker-compose up --build
```

4. Open your browser and go to: `http://localhost:5000`

### Option 2: Using Docker directly

1. Build the Docker image:

```bash
docker build -t document-analyst .
```

2. Run the container:

```bash
docker run -p 5000:5000 document-analyst
```

3. Open your browser and go to: `http://localhost:5000`

## Usage

1. **Upload Documents**: Upload 3-10 documents (PDF, DOCX, TXT)
2. **Select Persona**: Choose from predefined personas or create custom
3. **Define Objective**: Describe what you want to accomplish
4. **Process**: Click "Process Documents" to analyze
5. **Export**: Download results as "challenge1b_output.json"

## Features

- **Local Processing**: No internet required during analysis
- **Multiple Formats**: Supports PDF, DOCX, and TXT files
- **Fast Analysis**: Processes 3-10 documents in under 60 seconds
- **Lightweight**: Uses TF-IDF and scikit-learn (under 1GB model size)
- **Export Options**: JSON and CSV export formats

## Stopping the Application

- If using Docker Compose: `Ctrl+C` then `docker-compose down`
- If using Docker directly: `Ctrl+C` or `docker stop <container-id>`

## Troubleshooting

1. **Port already in use**: Change the port mapping in docker-compose.yml from "5000:5000" to "8501:5000"
2. **Memory issues**: Ensure Docker has at least 2GB RAM allocated
3. **Build issues**: Try `docker-compose build --no-cache`

## Development

For development with live code reloading, the docker-compose.yml includes volume mounting. Your local changes will be reflected in the container.

## System Requirements

- **RAM**: Minimum 2GB available for Docker
- **Storage**: ~1GB for Docker image and dependencies
- **CPU**: Any modern processor (multi-core recommended for faster processing)
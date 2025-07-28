# adobe25-challenge-1b-bingpot
An AI-powered document analysis tool that extracts and prioritizes relevant sections from document collections based on user personas and objectives. Built with Streamlit and designed for local deployment using Docker.
<img width="1569" height="597" alt="image" src="https://github.com/user-attachments/assets/722f39f0-b8ee-4b34-9a37-f9b4315f3998" />

## Features

- **Multi-Format Support**: Process PDF, DOCX, and TXT documents
- **Persona-Based Analysis**: Tailored content extraction based on user roles
- **Local Processing**: No internet required during analysis (uses TF-IDF and scikit-learn)
- **Fast Performance**: Processes 3-10 documents in under 60 seconds
- **Lightweight**: Uses models under 1GB total size
- **Export Options**: JSON and CSV export formats
- **Docker Ready**: Containerized for easy local deployment

## Quick Start

### Prerequisites

- Docker and Docker Compose installed on your system

### Run with Docker

1. Clone the repository:
```bash
git clone <repository-url>
cd intelligent-document-analyst
```

2. Start the application:
```bash
docker-compose up --build
```

3. Open your browser and navigate to:
```
http://localhost:8501
```

## Usage

### 1. Upload Documents
- Upload 3-10 documents (PDF, DOCX, or TXT format)
- Maximum file size depends on your system memory

### 2. Configure Analysis
- **Select Persona**: Choose from predefined options or create custom:
  - Travel Planner
  - Business Analyst
  - Research Scientist
  - Marketing Manager
  - Project Manager
  - Custom (define your own)

- **Define Objective**: Describe what you want to accomplish
  - Example: "Plan a trip of 4 days for a group of 10 college friends"

### 3. Process Documents
- Click "Process Documents" to start analysis
- Processing typically takes 10-45 seconds for 3-10 documents
- Progress bar shows real-time status

### 4. Review Results
- View ranked sections by relevance
- See detailed subsection analysis
- Check processing metadata and timing

### 5. Export Results
- **JSON Export**: Downloads as "challenge1b_output.json"
- **CSV Export**: Downloads with timestamp for spreadsheet analysis

## Output Format

The system generates structured JSON output with:

```json
{
  "metadata": {
    "input_documents": [],
    "persona": "",
    "job_to_be_done": "",
    "processing_timestamp": "",
    "processing_time": ""
  },
  "extracted_sections": [
    {
      "document": "",
      "section_title": "",
      "importance_rank": ,
      "page_number": ,
      "relevance_score":
    }
  ],
  "subsection_analysis": [
    {
      "document": "",
      "refined_text": "",
      "page_number": 
    }
  ]
}
```

## Technical Architecture

### Core Components

- **Document Processor**: Handles PDF, DOCX, and TXT file extraction
- **NLP Analyzer**: Uses TF-IDF vectorization for semantic similarity
- **Ranking Engine**: Combines semantic and keyword-based scoring
- **Export System**: Generates JSON and CSV outputs

### Processing Pipeline

1. **Text Extraction**: Format-specific extraction with page tracking
2. **Section Detection**: Pattern-based identification of document sections
3. **Semantic Analysis**: TF-IDF vectorization for relevance scoring
4. **Ranking**: Combined similarity and keyword-based prioritization
5. **Output Generation**: Structured results with metadata

### Dependencies

- **Streamlit**: Web application framework
- **scikit-learn**: TF-IDF vectorization and similarity computation
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX document processing
- **pandas**: Data manipulation and CSV export
- **numpy**: Numerical operations

### Project Structure

```
├── app.py                 # Main Streamlit application
├── document_processor.py  # Document text extraction
├── nlp_analyzer.py        # NLP analysis and ranking
├── utils.py              # Export utilities
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Docker Compose setup
├── pyproject.toml        # Python dependencies
└── .streamlit/
    └── config.toml       # Streamlit configuration
```

## Configuration

### Performance Tuning

- **Document Limit**: 3-10 documents (configurable in app.py)
- **Section Length**: Minimum 30 words (adjustable via slider)
- **Max Sections**: Up to 20 ranked sections (configurable)

### Docker Configuration

- **Port**: Application runs on port 5000 inside container, mapped to 8501 on host
- **Memory**: Recommend 2GB+ RAM for optimal performance
- **Health Checks**: Built-in monitoring for container health


### Performance Optimization

- Use documents with clear section structure for better results
- Upload at least 3 pdfs
- Optimal document size: 1-50 pages per document
- Clear, descriptive job objectives improve relevance scoring

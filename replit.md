# Intelligent Document Analyst

## Overview

The Intelligent Document Analyst is a Streamlit-based web application that processes document collections and extracts relevant sections based on user personas and objectives. The system uses natural language processing to analyze documents, rank content by relevance, and provide structured outputs for decision-making.

## User Preferences

Preferred communication style: Simple, everyday language.
Document upload limit: Allow 3-10 documents per analysis session (updated July 28, 2025).
JSON export filename: Use "challenge1b_output.json" as default filename (updated July 28, 2025).

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web application framework
- **Layout**: Wide layout with expandable sidebar for configuration
- **State Management**: Streamlit session state for maintaining processed results and completion status
- **User Interface**: Interactive sidebar for persona selection and configuration, main area for file uploads and results display

### Backend Architecture
- **Modular Design**: Separated into distinct processing modules
  - `DocumentProcessor`: Handles file format processing and text extraction
  - `NLPAnalyzer`: Performs natural language processing and section analysis
  - `utils`: Provides export functionality for results
- **Processing Pipeline**: Sequential document processing, NLP analysis, and result formatting

### Data Processing Components
- **Document Support**: PDF, DOCX, and TXT file formats
- **Text Extraction**: Format-specific extraction methods with error handling
- **Section Detection**: Pattern-based section identification using regex
- **Content Analysis**: Basic NLP processing with optional spaCy integration

## Key Components

### Document Processor (`document_processor.py`)
- **Purpose**: Extract text content from uploaded documents
- **Supported Formats**: PDF (PyPDF2), DOCX (python-docx), TXT (plain text)
- **Features**: Page number tracking, error handling, format validation
- **Architecture Decision**: Separate processing methods for each format to handle format-specific requirements

### NLP Analyzer (`nlp_analyzer.py`)
- **Purpose**: Analyze document text and extract meaningful sections
- **Processing Approach**: Pattern-based section detection using multiple regex patterns
- **Fallback Strategy**: Basic text processing when spaCy model is unavailable
- **Section Identification**: Detects headers, numbered sections, markdown headers, and page breaks

### Utility Functions (`utils.py`)
- **Purpose**: Export processed results in multiple formats
- **Supported Exports**: JSON and CSV formats
- **Data Structure**: Structured output including metadata, extracted sections, and subsection analysis

### Main Application (`app.py`)
- **Purpose**: Streamlit interface and user interaction management
- **Configuration**: Sidebar-based persona selection and custom input
- **Session Management**: Maintains processing state across user interactions
- **Result Display**: Structured presentation of analysis results

## Data Flow

1. **Input Stage**: Users upload document files through Streamlit interface
2. **Configuration**: Users select persona and define objectives in sidebar
3. **Document Processing**: Files are processed by `DocumentProcessor` to extract text
4. **NLP Analysis**: `NLPAnalyzer` processes text to identify and rank sections
5. **Result Compilation**: Structured results including metadata, sections, and analysis
6. **Output**: Results displayed in web interface with export options (JSON/CSV)

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for user interface
- **pandas**: Data manipulation and CSV export functionality
- **PyPDF2**: PDF text extraction
- **python-docx**: DOCX document processing
- **spaCy**: Advanced NLP processing (optional with fallback)

### Optional Dependencies
- **spacy model (en_core_web_sm)**: English language model for enhanced NLP processing
- **numpy**: Numerical operations for analysis scoring
- **collections**: Built-in Python module for data structures

## Deployment Strategy

### Current Setup
- **Platform**: Designed for local development and deployment
- **Dependencies**: Requires manual installation of required packages
- **spaCy Model**: Optional dependency with graceful fallback to basic processing

### Architecture Decisions
- **Modular Design**: Separated concerns for easier maintenance and testing
- **Error Handling**: Comprehensive error handling for document processing failures
- **Fallback Mechanisms**: Basic processing when advanced NLP libraries are unavailable
- **Export Options**: Multiple output formats to accommodate different use cases

### Scalability Considerations
- **Memory Management**: Processes documents sequentially to manage memory usage
- **File Size Limits**: No explicit limits implemented, relies on Streamlit defaults
- **Processing Time**: No asynchronous processing, suitable for moderate document collections

The system prioritizes simplicity and reliability over advanced features, making it accessible for users who need quick document analysis without complex setup requirements.
import json
import pandas as pd
from typing import Dict, Any
from io import StringIO

def export_results_to_json(results: Dict[str, Any]) -> str:
    """Export results to JSON format"""
    try:
        return json.dumps(results, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Error exporting to JSON: {str(e)}")
        return "{}"

def export_results_to_csv(results: Dict[str, Any]) -> str:
    """Export results to CSV format"""
    try:
        # Prepare data for CSV
        rows = []
        
        # Add metadata
        metadata = results.get('metadata', {})
        rows.append({
            'Type': 'Metadata',
            'Document': 'System',
            'Title': 'Processing Info',
            'Persona': metadata.get('persona', ''),
            'Job_To_Be_Done': metadata.get('job_to_be_done', ''),
            'Processing_Time': metadata.get('processing_time', ''),
            'Rank': '',
            'Page': '',
            'Relevance_Score': ''
        })
        
        # Add extracted sections
        for section in results.get('extracted_sections', []):
            rows.append({
                'Type': 'Section',
                'Document': section.get('document', ''),
                'Title': section.get('section_title', ''),
                'Persona': metadata.get('persona', ''),
                'Job_To_Be_Done': metadata.get('job_to_be_done', ''),
                'Processing_Time': '',
                'Rank': section.get('importance_rank', ''),
                'Page': section.get('page_number', ''),
                'Relevance_Score': section.get('relevance_score', '')
            })
        
        # Add subsection analysis
        for i, analysis in enumerate(results.get('subsection_analysis', [])):
            rows.append({
                'Type': 'Analysis',
                'Document': analysis.get('document', ''),
                'Title': f"Analysis {i+1}",
                'Persona': metadata.get('persona', ''),
                'Job_To_Be_Done': analysis.get('refined_text', '')[:100] + '...',
                'Processing_Time': '',
                'Rank': '',
                'Page': analysis.get('page_number', ''),
                'Relevance_Score': ''
            })
        
        # Convert to DataFrame and then CSV
        df = pd.DataFrame(rows)
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        return csv_buffer.getvalue()
        
    except Exception as e:
        print(f"Error exporting to CSV: {str(e)}")
        return "Error,Message\nExport Failed,Could not generate CSV"

def validate_file_type(filename: str) -> bool:
    """Validate if file type is supported"""
    supported_extensions = ['pdf', 'txt', 'docx']
    file_extension = filename.split('.')[-1].lower()
    return file_extension in supported_extensions

def format_processing_time(seconds: float) -> str:
    """Format processing time in human readable format"""
    if seconds < 1:
        return f"{seconds*1000:.0f}ms"
    elif seconds < 60:
        return f"{seconds:.1f}s"
    else:
        minutes = int(seconds // 60)
        remaining_seconds = seconds % 60
        return f"{minutes}m {remaining_seconds:.1f}s"

def truncate_text(text: str, max_length: int = 200) -> str:
    """Truncate text to specified length with ellipsis"""
    if not text:
        return ""
    
    if len(text) <= max_length:
        return text
    
    return text[:max_length-3] + "..."

def extract_filename_without_extension(filename: str) -> str:
    """Extract filename without extension"""
    return '.'.join(filename.split('.')[:-1])

def calculate_readability_score(text: str) -> float:
    """Calculate simple readability score based on sentence and word length"""
    if not text:
        return 0.0
    
    sentences = text.split('.')
    words = text.split()
    
    if len(sentences) == 0 or len(words) == 0:
        return 0.0
    
    avg_sentence_length = len(words) / len(sentences)
    avg_word_length = sum(len(word) for word in words) / len(words)
    
    # Simple readability formula (lower is better)
    score = 206.835 - (1.015 * avg_sentence_length) - (84.6 * avg_word_length / 5)
    return max(0, min(100, score))

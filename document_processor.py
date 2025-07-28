import PyPDF2
import docx
import io
import re
from typing import Optional, List, Dict

class DocumentProcessor:
    """Handles processing of various document formats"""
    
    def __init__(self):
        self.supported_formats = ['pdf', 'txt', 'docx']
    
    def process_file(self, uploaded_file) -> Optional[str]:
        """Process an uploaded file and extract text content"""
        try:
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                return self._process_pdf(uploaded_file)
            elif file_extension == 'txt':
                return self._process_txt(uploaded_file)
            elif file_extension == 'docx':
                return self._process_docx(uploaded_file)
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
                
        except Exception as e:
            print(f"Error processing file {uploaded_file.name}: {str(e)}")
            return None
    
    def _process_pdf(self, uploaded_file) -> str:
        """Extract text from PDF file"""
        try:
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Read PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text_content = []
            
            for page_num, page in enumerate(pdf_reader.pages):
                page_text = page.extract_text()
                if page_text.strip():
                    # Add page number marker for section tracking
                    text_content.append(f"[PAGE {page_num + 1}]\n{page_text}")
            
            return '\n\n'.join(text_content)
            
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return ""
    
    def _process_txt(self, uploaded_file) -> str:
        """Extract text from TXT file"""
        try:
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Try different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    uploaded_file.seek(0)
                    content = uploaded_file.read()
                    if isinstance(content, bytes):
                        text = content.decode(encoding)
                    else:
                        text = content
                    return text
                except UnicodeDecodeError:
                    continue
            
            # If all encodings fail, use utf-8 with error handling
            uploaded_file.seek(0)
            content = uploaded_file.read()
            if isinstance(content, bytes):
                return content.decode('utf-8', errors='replace')
            return content
            
        except Exception as e:
            print(f"Error processing TXT: {str(e)}")
            return ""
    
    def _process_docx(self, uploaded_file) -> str:
        """Extract text from DOCX file"""
        try:
            # Reset file pointer
            uploaded_file.seek(0)
            
            # Read DOCX
            doc = docx.Document(uploaded_file)
            text_content = []
            
            for para in doc.paragraphs:
                if para.text.strip():
                    text_content.append(para.text)
            
            return '\n\n'.join(text_content)
            
        except Exception as e:
            print(f"Error processing DOCX: {str(e)}")
            return ""
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        if not text:
            return ""
        
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text)
        
        # Remove excessive newlines
        text = re.sub(r'\n+', '\n', text)
        
        return text.strip()
    
    def extract_page_number(self, text_chunk: str) -> int:
        """Extract page number from text chunk"""
        page_match = re.search(r'\[PAGE (\d+)\]', text_chunk)
        if page_match:
            return int(page_match.group(1))
        return 1

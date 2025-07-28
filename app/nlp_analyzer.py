import re
from typing import List, Dict, Any
import numpy as np
from collections import Counter
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class NLPAnalyzer:
    """Handles NLP analysis and section extraction with lightweight models"""
    
    def __init__(self):
        # Initialize TF-IDF vectorizer for semantic similarity
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=1,
            max_df=0.95
        )
        print("NLP Analyzer initialized with TF-IDF vectorizer for local processing")
    
    def extract_sections(self, text: str, min_length: int = 30) -> List[Dict[str, Any]]:
        """Extract meaningful sections from document text"""
        if not text:
            return []
        
        sections = []
        
        # Split text into potential sections based on formatting cues
        section_patterns = [
            r'\n\s*[A-Z][^a-z\n]{10,}\s*\n',  # ALL CAPS headers
            r'\n\s*\d+\.\s+[A-Z][^\n]+\n',     # Numbered headers
            r'\n\s*[A-Z][^a-z\n]+:\s*\n',     # Colon-terminated headers
            r'\n\s*#{1,6}\s+[^\n]+\n',        # Markdown headers
            r'\[PAGE \d+\]'                    # Page breaks
        ]
        
        # Find section boundaries
        boundaries = [0]
        for pattern in section_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                boundaries.append(match.start())
        
        boundaries.append(len(text))
        boundaries = sorted(set(boundaries))
        
        # Extract sections
        for i in range(len(boundaries) - 1):
            start = boundaries[i]
            end = boundaries[i + 1]
            section_text = text[start:end].strip()
            
            if len(section_text.split()) >= min_length:
                # Extract title (first meaningful line)
                title = self._extract_title(section_text)
                
                # Extract page number
                page_number = self._extract_page_number(section_text)
                
                sections.append({
                    'title': title,
                    'content': section_text,
                    'page_number': page_number,
                    'word_count': len(section_text.split())
                })
        
        return sections
    
    def rank_sections(self, sections: List[Dict], persona: str, job_to_be_done: str, max_sections: int = 10) -> List[Dict]:
        """Rank sections based on relevance to persona and job using TF-IDF similarity"""
        if not sections:
            return []
        
        # Create query from persona and job
        query = f"{persona} {job_to_be_done}"
        
        # Prepare documents for TF-IDF analysis
        documents = [section['content'] for section in sections]
        all_docs = documents + [query]
        
        # Fit TF-IDF vectorizer and compute similarity
        try:
            tfidf_matrix = self.tfidf_vectorizer.fit_transform(all_docs)
            query_vector = tfidf_matrix[-1]  # Last document is the query
            document_vectors = tfidf_matrix[:-1]  # All except the query
            
            # Calculate cosine similarity between query and documents
            similarities = cosine_similarity(query_vector, document_vectors).flatten()
            
            # Score sections with combined approach
            scored_sections = []
            for i, section in enumerate(sections):
                # Base similarity score
                similarity_score = similarities[i] * 100  # Scale to 0-100
                
                # Add keyword-based scoring
                keyword_score = self._calculate_keyword_score(
                    section['content'], 
                    persona, 
                    job_to_be_done
                )
                
                # Combined score
                final_score = similarity_score * 0.7 + keyword_score * 0.3
                
                section['relevance_score'] = round(final_score, 2)
                scored_sections.append(section)
            
        except Exception as e:
            print(f"Error in TF-IDF ranking: {str(e)}")
            # Fallback to keyword-based scoring only
            scored_sections = []
            for section in sections:
                score = self._calculate_keyword_score(
                    section['content'], 
                    persona, 
                    job_to_be_done
                )
                section['relevance_score'] = score
                scored_sections.append(section)
        
        # Sort by relevance score (descending)
        scored_sections.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return scored_sections[:max_sections]
    
    def analyze_subsection(self, text: str) -> Dict[str, Any]:
        """Analyze a subsection and provide summary"""
        if not text:
            return {'summary': '', 'keywords': []}
        
        # Extract key sentences
        sentences = self._split_sentences(text)
        
        # Get most important sentences (up to 3)
        important_sentences = self._get_important_sentences(sentences, max_sentences=3)
        
        # Extract keywords
        keywords = self._extract_keywords(text)
        
        return {
            'summary': ' '.join(important_sentences),
            'keywords': keywords[:10]  # Top 10 keywords
        }
    
    def _extract_title(self, text: str) -> str:
        """Extract a meaningful title from section text"""
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and len(line.split()) >= 2 and len(line.split()) <= 15:
                # Clean up the title
                title = re.sub(r'\[PAGE \d+\]', '', line).strip()
                title = re.sub(r'^\d+\.\s*', '', title)  # Remove numbering
                title = re.sub(r':$', '', title)        # Remove trailing colon
                
                if title:
                    return title
        
        # Fallback: use first few words
        words = text.split()[:8]
        return ' '.join(words) + ('...' if len(text.split()) > 8 else '')
    
    def _extract_page_number(self, text: str) -> int:
        """Extract page number from text"""
        page_match = re.search(r'\[PAGE (\d+)\]', text)
        if page_match:
            return int(page_match.group(1))
        return 1
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text using basic NLP"""
        if not text:
            return []
        
        # Clean text
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among', 'under', 'over', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
            'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those'
        }
        
        # Filter words
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        
        # Count frequency
        word_freq = Counter(keywords)
        
        # Return most frequent words
        return [word for word, freq in word_freq.most_common(20)]
    
    def _calculate_keyword_score(self, content: str, persona: str, job: str) -> float:
        """Calculate keyword-based relevance score for content"""
        if not content:
            return 0.0
        
        content_lower = content.lower()
        score = 0.0
        
        # Job-specific keywords (highest weight)
        job_keywords = self._extract_keywords(job)
        for keyword in job_keywords:
            if keyword.lower() in content_lower:
                count = content_lower.count(keyword.lower())
                tf = count / len(content.split())
                score += tf * 15  # High weight for job keywords
        
        # Persona-specific keywords
        persona_keywords = self._get_persona_keywords(persona)
        for keyword in persona_keywords:
            if keyword.lower() in content_lower:
                score += 8.0
        
        # Section quality bonus
        word_count = len(content.split())
        if 50 <= word_count <= 500:  # Optimal section length
            score += 2.0
        elif word_count > 500:
            score += math.log(word_count / 500)
        
        return round(score, 2)
    
    def _get_persona_keywords(self, persona: str) -> List[str]:
        """Get keywords relevant to specific personas"""
        persona_map = {
            'Travel Planner': ['travel', 'trip', 'destination', 'hotel', 'restaurant', 'activity', 'tour', 'visit', 'explore'],
            'Business Analyst': ['business', 'market', 'analysis', 'data', 'revenue', 'strategy', 'competitive', 'trend'],
            'Research Scientist': ['research', 'study', 'method', 'data', 'analysis', 'findings', 'experiment', 'results'],
            'Marketing Manager': ['marketing', 'campaign', 'audience', 'brand', 'promotion', 'advertising', 'customer'],
            'Project Manager': ['project', 'timeline', 'requirements', 'deliverable', 'milestone', 'resource', 'planning']
        }
        
        return persona_map.get(persona, [])
    
    def _get_job_keywords(self, job: str) -> List[str]:
        """Extract keywords from job description"""
        return self._extract_keywords(job)[:10]
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _get_important_sentences(self, sentences: List[str], max_sentences: int = 3) -> List[str]:
        """Get most important sentences from a list"""
        if not sentences:
            return []
        
        # Score sentences by length and keyword density
        scored_sentences = []
        
        for sentence in sentences:
            if len(sentence.split()) < 5:  # Skip very short sentences
                continue
                
            score = len(sentence.split())  # Length factor
            
            # Add keyword bonus
            keywords = self._extract_keywords(sentence)
            score += len(keywords) * 2
            
            scored_sentences.append((sentence, score))
        
        # Sort by score and return top sentences
        scored_sentences.sort(key=lambda x: x[1], reverse=True)
        
        return [sentence for sentence, score in scored_sentences[:max_sentences]]

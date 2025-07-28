import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
from io import BytesIO
import zipfile
from document_processor import DocumentProcessor
from nlp_analyzer import NLPAnalyzer
from utils import export_results_to_json, export_results_to_csv

# Configure page
st.set_page_config(
    page_title="Intelligent Document Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'processed_results' not in st.session_state:
    st.session_state.processed_results = None
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False

def main():
    st.title("🔍 Intelligent Document Analyst")
    st.markdown("Extract and prioritize relevant sections from document collections based on personas and objectives")
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Persona selection
        st.subheader("👤 Persona")
        persona_options = [
            "Travel Planner",
            "Business Analyst", 
            "Research Scientist",
            "Marketing Manager",
            "Project Manager",
            "Custom"
        ]
        selected_persona = st.selectbox("Select Persona", persona_options)
        
        if selected_persona == "Custom":
            custom_persona = st.text_input("Enter custom persona")
            persona = custom_persona if custom_persona else "Custom User"
        else:
            persona = selected_persona
            
        # Job to be done
        st.subheader("🎯 Job to be Done")
        job_examples = {
            "Travel Planner": "Plan a trip of 4 days for a group of 10 college friends",
            "Business Analyst": "Analyze market trends and competitive landscape",
            "Research Scientist": "Extract key findings and methodologies",
            "Marketing Manager": "Identify target audience and marketing strategies",
            "Project Manager": "Extract project requirements and timelines"
        }
        
        placeholder_text = job_examples.get(selected_persona, "Describe what you want to accomplish...")
        job_to_be_done = st.text_area(
            "Describe your objective",
            placeholder=placeholder_text,
            height=100
        )
        
        # Processing options
        st.subheader("⚙️ Processing Options")
        max_sections = st.slider("Max sections to extract", 3, 20, 10)
        min_section_length = st.slider("Min section length (words)", 10, 100, 30)
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.header("📁 Document Upload")
        
        uploaded_files = st.file_uploader(
            "Upload documents (PDF, TXT, DOCX)",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            help="Upload 3-10 documents for analysis"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} files uploaded")
            
            # Display uploaded files
            with st.expander("📋 Uploaded Files", expanded=True):
                for file in uploaded_files:
                    st.write(f"• {file.name} ({file.size / 1024:.1f} KB)")
        
        # Processing button
        if st.button("🚀 Process Documents", type="primary", disabled=not uploaded_files or not job_to_be_done):
            if len(uploaded_files) < 3:
                st.warning("⚠️ Please upload at least 3 documents for optimal analysis")
            elif len(uploaded_files) > 10:
                st.warning("⚠️ For optimal performance, please upload no more than 10 documents")
            else:
                process_documents(uploaded_files, persona, job_to_be_done, max_sections, min_section_length)
    
    with col2:
        st.header("📊 Results")
        
        if st.session_state.processing_complete and st.session_state.processed_results:
            display_results(st.session_state.processed_results)
        else:
            st.info("Upload documents and click 'Process Documents' to see results")

def process_documents(uploaded_files, persona, job_to_be_done, max_sections, min_section_length):
    """Process uploaded documents and extract relevant sections"""
    
    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    start_time = time.time()
    
    try:
        # Initialize processors
        doc_processor = DocumentProcessor()
        nlp_analyzer = NLPAnalyzer()
        
        status_text.text("📄 Processing documents...")
        progress_bar.progress(10)
        
        # Process all documents
        all_documents = []
        for i, file in enumerate(uploaded_files):
            status_text.text(f"📄 Processing {file.name}...")
            doc_content = doc_processor.process_file(file)
            if doc_content:
                all_documents.append({
                    'filename': file.name,
                    'content': doc_content
                })
            progress_bar.progress(10 + (i + 1) * 30 // len(uploaded_files))
        
        if not all_documents:
            st.error("❌ No documents could be processed successfully")
            return
            
        status_text.text("🔍 Extracting sections...")
        progress_bar.progress(50)
        
        # Extract sections from all documents
        all_sections = []
        for doc in all_documents:
            sections = nlp_analyzer.extract_sections(doc['content'], min_section_length)
            for section in sections:
                section['document'] = doc['filename']
                all_sections.append(section)
        
        status_text.text("🎯 Ranking sections by relevance...")
        progress_bar.progress(70)
        
        # Rank sections based on persona and job
        ranked_sections = nlp_analyzer.rank_sections(
            all_sections, 
            persona, 
            job_to_be_done, 
            max_sections
        )
        
        status_text.text("📋 Analyzing subsections...")
        progress_bar.progress(85)
        
        # Analyze top sections for subsection details
        subsection_analysis = []
        for section in ranked_sections[:5]:  # Analyze top 5 sections
            analysis = nlp_analyzer.analyze_subsection(section['content'])
            subsection_analysis.append({
                'document': section['document'],
                'refined_text': analysis['summary'],
                'page_number': section.get('page_number', 1)
            })
        
        progress_bar.progress(100)
        processing_time = time.time() - start_time
        
        # Prepare results
        results = {
            'metadata': {
                'input_documents': [doc['filename'] for doc in all_documents],
                'persona': persona,
                'job_to_be_done': job_to_be_done,
                'processing_timestamp': datetime.now().isoformat(),
                'processing_time': f"{processing_time:.2f} seconds"
            },
            'extracted_sections': [
                {
                    'document': section['document'],
                    'section_title': section['title'],
                    'importance_rank': i + 1,
                    'page_number': section.get('page_number', 1),
                    'relevance_score': section['relevance_score']
                }
                for i, section in enumerate(ranked_sections)
            ],
            'subsection_analysis': subsection_analysis
        }
        
        st.session_state.processed_results = results
        st.session_state.processing_complete = True
        
        status_text.text(f"✅ Processing complete in {processing_time:.2f} seconds")
        
        if processing_time > 60:
            st.warning(f"⚠️ Processing took {processing_time:.2f} seconds (target: <60s)")
        else:
            st.success(f"🎉 Processing completed in {processing_time:.2f} seconds")
            
    except Exception as e:
        st.error(f"❌ Error during processing: {str(e)}")
        progress_bar.progress(0)
        status_text.text("Processing failed")

def display_results(results):
    """Display the processed results"""
    
    # Metadata summary
    with st.expander("📋 Processing Summary", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Documents Processed", len(results['metadata']['input_documents']))
        with col2:
            st.metric("Sections Extracted", len(results['extracted_sections']))
        with col3:
            st.metric("Processing Time", results['metadata']['processing_time'])
        
        st.write("**Persona:**", results['metadata']['persona'])
        st.write("**Objective:**", results['metadata']['job_to_be_done'])
    
    # Extracted sections
    st.subheader("🎯 Ranked Sections")
    
    for section in results['extracted_sections']:
        with st.container():
            col1, col2, col3 = st.columns([1, 6, 2])
            
            with col1:
                st.markdown(f"**#{section['importance_rank']}**")
            
            with col2:
                st.markdown(f"**{section['section_title']}**")
                st.caption(f"Document: {section['document']} | Page: {section['page_number']}")
            
            with col3:
                score = section.get('relevance_score', 0)
                st.metric("Relevance", f"{score:.2f}")
            
            st.divider()
    
    # Subsection analysis
    if results.get('subsection_analysis'):
        st.subheader("📝 Detailed Analysis")
        
        for i, analysis in enumerate(results['subsection_analysis']):
            with st.expander(f"Analysis {i+1}: {analysis['document']}", expanded=False):
                st.write("**Page:**", analysis['page_number'])
                st.write("**Summary:**")
                st.write(analysis['refined_text'])
    
    # Export options
    st.subheader("💾 Export Results")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📄 Export as JSON"):
            json_data = export_results_to_json(results)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name="challenge1b_output.json",
                mime="application/json"
            )
    
    with col2:
        if st.button("📊 Export as CSV"):
            csv_data = export_results_to_csv(results)
            st.download_button(
                label="📥 Download CSV",
                data=csv_data,
                file_name=f"document_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()

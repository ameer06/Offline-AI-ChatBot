"""
PDF Processor for RAG System
=============================
Extracts and processes text from PDF documents
"""

import PyPDF2
from typing import List, Dict, Tuple
from pathlib import Path


class PDFProcessor:
    """Handles PDF text extraction and chunking"""
    
    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 50):
        """
        Initialize PDF processor
        
        Args:
            chunk_size: Number of characters per chunk
            chunk_overlap: Number of characters to overlap between chunks
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_from_pdf(self, pdf_path: str) -> Tuple[str, int]:
        """
        Extract all text from a PDF file
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Tuple of (extracted_text, page_count)
        """
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                page_count = len(pdf_reader.pages)
                
                text = ""
                for page_num in range(page_count):
                    page = pdf_reader.pages[page_num]
                    text += page.extract_text() + "\n"
                
                print(f"✅ Extracted {len(text)} characters from {page_count} pages")
                return text, page_count
                
        except Exception as e:
            print(f"❌ Error extracting text from PDF: {str(e)}")
            raise
    
    def chunk_text(self, text: str) -> List[Dict]:
        """
        Split text into overlapping chunks
        
        Args:
            text: The text to chunk
            
        Returns:
            List of chunk dictionaries with text and metadata
        """
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            # Get chunk end position
            end = start + self.chunk_size
            
            # Get the chunk text
            chunk_text = text[start:end]
            
            # Skip empty chunks
            if chunk_text.strip():
                chunks.append({
                    'id': chunk_id,
                    'text': chunk_text,
                    'start_char': start,
                    'end_char': min(end, len(text)),
                    'length': len(chunk_text)
                })
                chunk_id += 1
            
            # Move to next chunk with overlap
            start += (self.chunk_size - self.chunk_overlap)
        
        print(f"✅ Created {len(chunks)} chunks")
        return chunks
    
    def process_pdf(self, pdf_path: str) -> Dict:
        """
        Complete PDF processing pipeline
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with extracted text, chunks, and metadata
        """
        # Extract text
        text, page_count = self.extract_text_from_pdf(pdf_path)
        
        # Create chunks
        chunks = self.chunk_text(text)
        
        # Get file info
        pdf_file = Path(pdf_path)
        file_size = pdf_file.stat().st_size
        
        return {
            'filename': pdf_file.name,
            'file_path': str(pdf_path),
            'file_size': file_size,
            'page_count': page_count,
            'full_text': text,
            'text_length': len(text),
            'chunks': chunks,
            'chunk_count': len(chunks)
        }


# Test the processor if run directly
if __name__ == "__main__":
    print("PDF Processor initialized")
    print("Ready to process PDFs!")
    
    # Example usage (uncomment to test with actual PDF):
    # processor = PDFProcessor(chunk_size=512, chunk_overlap=50)
    # result = processor.process_pdf("path/to/your/file.pdf")
    # print(f"Processed: {result['filename']}")
    # print(f"Pages: {result['page_count']}")
    # print(f"Chunks: {result['chunk_count']}")

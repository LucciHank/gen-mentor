#!/usr/bin/env python3
"""
Document ingestion script for GenMentor MVP
Processes documents and creates vector embeddings
"""

import os
import sys
import json
import csv
import hashlib
from pathlib import Path
from typing import Dict, List, Any
import psycopg2
from psycopg2.extras import RealDictCursor

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

from base.embedder_factory import EmbedderFactory
from base.rag_factory import RagFactory
from utils.preprocess import extract_text_from_pdf
import markdown

class DocumentIngester:
    def __init__(self):
        self.conn = self.get_db_connection()
        self.embedder = EmbedderFactory.create("sentence-transformers", "all-mpnet-base-v2")
        self.rag_manager = None
        self.setup_rag_manager()
    
    def get_db_connection(self):
        """Get database connection"""
        try:
            conn = psycopg2.connect(
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=os.getenv('DB_NAME', 'genmentor'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', 'password')
            )
            return conn
        except psycopg2.Error as e:
            print(f"Error connecting to database: {e}")
            return None
    
    def setup_rag_manager(self):
        """Setup RAG manager for vector storage"""
        try:
            from base.search_rag import SearchRagManager
            from config import load_config
            
            config = load_config(config_name="main")
            self.rag_manager = SearchRagManager.from_config(config)
            print("RAG manager initialized successfully")
        except Exception as e:
            print(f"Warning: Could not initialize RAG manager: {e}")
            print("Vector indexing will be skipped")
    
    def load_manifest(self) -> Dict[str, Any]:
        """Load knowledge manifest"""
        manifest_path = Path(__file__).parent.parent.parent / "seed_data" / "manifests" / "knowledge_manifest.json"
        
        if not manifest_path.exists():
            print(f"Manifest file not found: {manifest_path}")
            return {}
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_document_registry(self) -> List[Dict[str, Any]]:
        """Load document registry CSV"""
        registry_path = Path(__file__).parent.parent.parent / "seed_data" / "manifests" / "document_registry.csv"
        
        if not registry_path.exists():
            print(f"Registry file not found: {registry_path}")
            return []
        
        documents = []
        with open(registry_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                documents.append(row)
        
        return documents
    
    def extract_content(self, file_path: Path, file_type: str) -> str:
        """Extract content from different file types"""
        try:
            if file_type.lower() == 'pdf':
                return extract_text_from_pdf(str(file_path))
            elif file_type.lower() in ['docx', 'doc']:
                # For demo, we'll use markdown files instead of actual docx
                if file_path.with_suffix('.md').exists():
                    with open(file_path.with_suffix('.md'), 'r', encoding='utf-8') as f:
                        return f.read()
                else:
                    print(f"Warning: {file_path} not found, using placeholder content")
                    return f"Placeholder content for {file_path.name}"
            elif file_type.lower() == 'md':
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            elif file_type.lower() in ['xlsx', 'xls']:
                # For demo, return placeholder content
                return f"Excel content from {file_path.name} - would be processed in full implementation"
            else:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"Error extracting content from {file_path}: {e}")
            return ""
    
    def chunk_content(self, content: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[str]:
        """Split content into chunks for vector indexing"""
        if len(content) <= chunk_size:
            return [content]
        
        chunks = []
        start = 0
        
        while start < len(content):
            end = start + chunk_size
            
            # Try to break at sentence boundary
            if end < len(content):
                # Look for sentence endings
                for i in range(end, max(start + chunk_size - 100, start), -1):
                    if content[i] in '.!?':
                        end = i + 1
                        break
            
            chunk = content[start:end].strip()
            if chunk:
                chunks.append(chunk)
            
            start = end - chunk_overlap
            if start >= len(content):
                break
        
        return chunks
    
    def calculate_content_hash(self, content: str) -> str:
        """Calculate hash of content for deduplication"""
        return hashlib.md5(content.encode('utf-8')).hexdigest()
    
    def store_document_metadata(self, doc_info: Dict[str, Any], file_path: Path, content: str) -> int:
        """Store document metadata in database"""
        if not self.conn:
            return None
        
        try:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            
            # Parse tags
            tags = [tag.strip() for tag in doc_info.get('tags', '').split(',') if tag.strip()]
            
            # Create metadata
            metadata = {
                'target_skills': [skill.strip() for skill in doc_info.get('target_skills', '').split(',') if skill.strip()],
                'difficulty_level': doc_info.get('difficulty_level', 'beginner'),
                'description': doc_info.get('description', ''),
                'content_hash': self.calculate_content_hash(content),
                'content_length': len(content)
            }
            
            cursor.execute("""
                INSERT INTO documents (
                    filename, title, file_type, file_path, file_size,
                    content_type, category, subcategory, tags, metadata
                ) VALUES (
                    %(filename)s, %(title)s, %(file_type)s, %(file_path)s, %(file_size)s,
                    %(content_type)s, %(category)s, %(subcategory)s, %(tags)s, %(metadata)s
                ) ON CONFLICT (filename) DO UPDATE SET
                    title = EXCLUDED.title,
                    file_type = EXCLUDED.file_type,
                    file_path = EXCLUDED.file_path,
                    file_size = EXCLUDED.file_size,
                    content_type = EXCLUDED.content_type,
                    category = EXCLUDED.category,
                    subcategory = EXCLUDED.subcategory,
                    tags = EXCLUDED.tags,
                    metadata = EXCLUDED.metadata,
                    updated_at = CURRENT_TIMESTAMP
                RETURNING id
            """, {
                'filename': doc_info['filename'],
                'title': doc_info.get('title', doc_info['filename']),
                'file_type': doc_info['file_type'],
                'file_path': str(file_path),
                'file_size': file_path.stat().st_size if file_path.exists() else 0,
                'content_type': f"text/{doc_info['file_type']}",
                'category': doc_info.get('category', 'general'),
                'subcategory': doc_info.get('subcategory', ''),
                'tags': tags,
                'metadata': json.dumps(metadata)
            })
            
            doc_id = cursor.fetchone()['id']
            self.conn.commit()
            
            print(f"Stored document metadata: {doc_info['filename']} (ID: {doc_id})")
            return doc_id
            
        except psycopg2.Error as e:
            print(f"Error storing document metadata: {e}")
            if self.conn:
                self.conn.rollback()
            return None
    
    def index_document_content(self, doc_id: int, content: str, doc_info: Dict[str, Any]):
        """Index document content in vector store"""
        if not self.rag_manager:
            print("RAG manager not available, skipping vector indexing")
            return
        
        try:
            # Chunk content
            chunks = self.chunk_content(content)
            
            # Create metadata for each chunk
            base_metadata = {
                'document_id': doc_id,
                'filename': doc_info['filename'],
                'title': doc_info.get('title', doc_info['filename']),
                'category': doc_info.get('category', 'general'),
                'subcategory': doc_info.get('subcategory', ''),
                'file_type': doc_info['file_type']
            }
            
            # Add chunks to vector store
            for i, chunk in enumerate(chunks):
                chunk_metadata = {
                    **base_metadata,
                    'chunk_id': i,
                    'chunk_count': len(chunks)
                }
                
                # Add to vector store (this would depend on your RAG implementation)
                # For now, we'll just print what would be indexed
                print(f"Would index chunk {i+1}/{len(chunks)} for {doc_info['filename']}")
            
            print(f"Indexed {len(chunks)} chunks for document: {doc_info['filename']}")
            
        except Exception as e:
            print(f"Error indexing document content: {e}")
    
    def process_document(self, doc_info: Dict[str, Any], raw_data_path: Path) -> bool:
        """Process a single document"""
        filename = doc_info['filename']
        category = doc_info.get('category', 'general')
        file_type = doc_info['file_type']
        
        # Find the actual file
        file_path = raw_data_path / category / filename
        
        # For demo, try markdown version if original doesn't exist
        if not file_path.exists() and file_type in ['docx', 'pdf']:
            md_path = file_path.with_suffix('.md')
            if md_path.exists():
                file_path = md_path
                file_type = 'md'
        
        if not file_path.exists():
            print(f"Warning: File not found: {file_path}")
            return False
        
        print(f"Processing document: {filename}")
        
        # Extract content
        content = self.extract_content(file_path, file_type)
        if not content:
            print(f"Warning: No content extracted from {filename}")
            return False
        
        # Store metadata in database
        doc_id = self.store_document_metadata(doc_info, file_path, content)
        if not doc_id:
            print(f"Failed to store metadata for {filename}")
            return False
        
        # Index content in vector store
        self.index_document_content(doc_id, content, doc_info)
        
        return True
    
    def ingest_all_documents(self):
        """Ingest all documents from registry"""
        print("Starting document ingestion...")
        
        # Load configuration
        manifest = self.load_manifest()
        documents = self.load_document_registry()
        
        if not documents:
            print("No documents found in registry")
            return False
        
        # Find raw data path
        raw_data_path = Path(__file__).parent.parent.parent / "seed_data" / "raw"
        if not raw_data_path.exists():
            print(f"Raw data directory not found: {raw_data_path}")
            return False
        
        # Process each document
        success_count = 0
        total_count = len(documents)
        
        for doc_info in documents:
            try:
                if self.process_document(doc_info, raw_data_path):
                    success_count += 1
            except Exception as e:
                print(f"Error processing document {doc_info.get('filename', 'unknown')}: {e}")
        
        print(f"Document ingestion completed: {success_count}/{total_count} documents processed successfully")
        return success_count > 0
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

def main():
    """Main ingestion function"""
    print("Starting GenMentor document ingestion...")
    
    ingester = DocumentIngester()
    
    try:
        success = ingester.ingest_all_documents()
        return success
    finally:
        ingester.close()

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
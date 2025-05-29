#!/usr/bin/env python3
"""
RAG System for Repository Analysis

This module implements a Retrieval-Augmented Generation (RAG) system
for answering questions about the repository based on its documentation
and analysis results.
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import faiss
import numpy as np
from pathlib import Path
import re

from openai_config import get_client, OpenAIClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Constants
VECTOR_STORE_PATH = "vector_store.faiss"
DOCUMENT_STORE_PATH = "document_store.json"
EMBEDDING_DIMENSION = 1536  # OpenAI embedding dimension

class RAGSystem:
    def __init__(self, openai_client: Optional[OpenAIClient] = None):
        """
        Initialize the RAG System.
        
        Args:
            openai_client: OpenAI client instance. If None, uses the default client.
        """
        try:
            self.openai_client = openai_client or get_client()
        except ValueError as e:
            logger.error(f"Error initializing OpenAI client: {str(e)}")
            self.openai_client = None
            
        self.index = None
        self.documents = {}
        
    def initialize(self, force: bool = False):
        """
        Initialize the vector store and document store.
        
        Args:
            force: If True, reinitialize even if the stores already exist.
        """
        if os.path.exists(VECTOR_STORE_PATH) and os.path.exists(DOCUMENT_STORE_PATH) and not force:
            logger.info("Loading existing vector store and document store")
            self.load()
            return True
        
        logger.info("Initializing new vector store and document store")
        
        # Create a new FAISS index
        self.index = faiss.IndexFlatL2(EMBEDDING_DIMENSION)
        self.documents = {}
        
        # Process repository documentation
        self._process_repository_documentation()
        
        # Process analysis reports
        self._process_analysis_reports()
        
        # Save the index and documents
        self.save()
        
        return True
    
    def _process_repository_documentation(self):
        """Process repository documentation files"""
        logger.info("Processing repository documentation")
        
        # Process README.md
        readme_path = Path("README.md")
        if readme_path.exists():
            with open(readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
                
            # Split README into chunks
            chunks = self._chunk_text(readme_content, chunk_size=1000, overlap=200)
            
            # Add chunks to the document store
            for i, chunk in enumerate(chunks):
                doc_id = f"readme_{i}"
                self.documents[doc_id] = {
                    "content": chunk,
                    "source": "README.md",
                    "chunk_id": i,
                    "metadata": {
                        "type": "documentation",
                        "file": "README.md"
                    }
                }
                
                # Generate embedding and add to index
                if self.openai_client:
                    embedding = self._get_embedding(chunk)
                    if embedding is not None:
                        if len(self.documents) == 1:  # First document
                            self.index = faiss.IndexFlatL2(len(embedding))
                            self.index.add(np.array([embedding], dtype=np.float32))
                        else:
                            self.index.add(np.array([embedding], dtype=np.float32))
        
        # Process other documentation files
        doc_files = list(Path(".").glob("**/*.md"))
        for doc_file in doc_files:
            if doc_file.name == "README.md":
                continue  # Already processed
                
            if ".git" in str(doc_file):
                continue  # Skip git files
                
            try:
                with open(doc_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Split into chunks
                chunks = self._chunk_text(content, chunk_size=1000, overlap=200)
                
                # Add chunks to the document store
                for i, chunk in enumerate(chunks):
                    doc_id = f"{doc_file.stem}_{i}"
                    self.documents[doc_id] = {
                        "content": chunk,
                        "source": str(doc_file),
                        "chunk_id": i,
                        "metadata": {
                            "type": "documentation",
                            "file": str(doc_file)
                        }
                    }
                    
                    # Generate embedding and add to index
                    if self.openai_client:
                        embedding = self._get_embedding(chunk)
                        if embedding is not None:
                            self.index.add(np.array([embedding], dtype=np.float32))
            except Exception as e:
                logger.error(f"Error processing {doc_file}: {str(e)}")
    
    def _process_analysis_reports(self):
        """Process analysis reports"""
        logger.info("Processing analysis reports")
        
        # Process Mistral analysis report
        mistral_report_path = Path("analysis_report.json")
        if mistral_report_path.exists():
            try:
                with open(mistral_report_path, 'r', encoding='utf-8') as f:
                    mistral_report = json.load(f)
                
                # Extract relevant sections
                if "mistral_analysis" in mistral_report:
                    analysis = mistral_report["mistral_analysis"]
                    
                    # Process each section
                    sections = {
                        "repository_type": analysis.get("repository_type", ""),
                        "primary_purpose": analysis.get("primary_purpose", ""),
                        "technology_stack": ", ".join(analysis.get("technology_stack", [])),
                        "code_quality": json.dumps(analysis.get("code_quality_assessment", {}), indent=2),
                        "security_analysis": json.dumps(analysis.get("security_analysis", {}), indent=2),
                        "recommendations": "\n".join([f"- {rec}" for rec in analysis.get("recommendations", [])]),
                        "complexity_score": analysis.get("complexity_score", ""),
                        "maintainability_score": analysis.get("maintainability_score", ""),
                        "scalability_potential": analysis.get("scalability_potential", "")
                    }
                    
                    # Add each section to the document store
                    for section_name, content in sections.items():
                        if content:
                            doc_id = f"mistral_{section_name}"
                            self.documents[doc_id] = {
                                "content": content,
                                "source": "Mistral Analysis",
                                "section": section_name,
                                "metadata": {
                                    "type": "analysis",
                                    "tool": "mistral",
                                    "section": section_name
                                }
                            }
                            
                            # Generate embedding and add to index
                            if self.openai_client:
                                embedding = self._get_embedding(content)
                                if embedding is not None:
                                    self.index.add(np.array([embedding], dtype=np.float32))
            except Exception as e:
                logger.error(f"Error processing Mistral analysis report: {str(e)}")
        
        # Process OpenAI analysis report
        openai_report_path = Path("openai_analysis_report.json")
        if openai_report_path.exists():
            try:
                with open(openai_report_path, 'r', encoding='utf-8') as f:
                    openai_report = json.load(f)
                
                # Extract relevant sections
                if "openai_analysis" in openai_report:
                    analysis = openai_report["openai_analysis"]
                    
                    # Process each section
                    sections = {
                        "repository_type": analysis.get("repository_type", ""),
                        "primary_purpose": analysis.get("primary_purpose", ""),
                        "technology_stack": ", ".join(analysis.get("technology_stack", [])),
                        "code_quality": json.dumps(analysis.get("code_quality_assessment", {}), indent=2),
                        "security_analysis": json.dumps(analysis.get("security_analysis", {}), indent=2),
                        "recommendations": "\n".join([f"- {rec}" for rec in analysis.get("recommendations", [])]),
                        "complexity_score": analysis.get("complexity_score", ""),
                        "maintainability_score": analysis.get("maintainability_score", ""),
                        "scalability_potential": analysis.get("scalability_potential", "")
                    }
                    
                    # Add each section to the document store
                    for section_name, content in sections.items():
                        if content:
                            doc_id = f"openai_{section_name}"
                            self.documents[doc_id] = {
                                "content": content,
                                "source": "OpenAI Analysis",
                                "section": section_name,
                                "metadata": {
                                    "type": "analysis",
                                    "tool": "openai",
                                    "section": section_name
                                }
                            }
                            
                            # Generate embedding and add to index
                            if self.openai_client:
                                embedding = self._get_embedding(content)
                                if embedding is not None:
                                    self.index.add(np.array([embedding], dtype=np.float32))
            except Exception as e:
                logger.error(f"Error processing OpenAI analysis report: {str(e)}")
        
        # Process comparison report
        comparison_report_path = Path("comparison_report.json")
        if comparison_report_path.exists():
            try:
                with open(comparison_report_path, 'r', encoding='utf-8') as f:
                    comparison_report = json.load(f)
                
                # Extract summary
                if "summary" in comparison_report:
                    summary = comparison_report["summary"]
                    
                    # Process summary sections
                    sections = {
                        "overall_agreement": json.dumps(summary.get("overall_agreement", {}), indent=2),
                        "key_differences": "\n".join([f"- {diff}" for diff in summary.get("key_differences", [])]),
                        "key_agreements": "\n".join([f"- {agree}" for agree in summary.get("key_agreements", [])]),
                        "conclusion": summary.get("conclusion", "")
                    }
                    
                    # Add each section to the document store
                    for section_name, content in sections.items():
                        if content:
                            doc_id = f"comparison_{section_name}"
                            self.documents[doc_id] = {
                                "content": content,
                                "source": "Comparison Analysis",
                                "section": section_name,
                                "metadata": {
                                    "type": "comparison",
                                    "section": section_name
                                }
                            }
                            
                            # Generate embedding and add to index
                            if self.openai_client:
                                embedding = self._get_embedding(content)
                                if embedding is not None:
                                    self.index.add(np.array([embedding], dtype=np.float32))
            except Exception as e:
                logger.error(f"Error processing comparison report: {str(e)}")
    
    def _chunk_text(self, text: str, chunk_size: int = 1000, overlap: int = 200) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to split.
            chunk_size: Maximum characters per chunk.
            overlap: Number of characters to overlap between chunks.
            
        Returns:
            List of text chunks.
        """
        if not text:
            return []
            
        # Split by paragraphs first
        paragraphs = text.split("\n\n")
        chunks = []
        current_chunk = ""
        
        for paragraph in paragraphs:
            # If adding this paragraph would exceed chunk size, save current chunk and start a new one
            if len(current_chunk) + len(paragraph) > chunk_size and current_chunk:
                chunks.append(current_chunk)
                # Start new chunk with overlap from the end of the previous chunk
                if len(current_chunk) > overlap:
                    current_chunk = current_chunk[-overlap:] + "\n\n" + paragraph
                else:
                    current_chunk = paragraph
            else:
                if current_chunk:
                    current_chunk += "\n\n" + paragraph
                else:
                    current_chunk = paragraph
        
        # Add the last chunk if it's not empty
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _get_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get embedding for text using OpenAI API.
        
        Args:
            text: Text to embed.
            
        Returns:
            Embedding vector or None if failed.
        """
        if not self.openai_client:
            logger.warning("OpenAI client not available, skipping embedding generation")
            # Return a random embedding for testing
            return np.random.rand(EMBEDDING_DIMENSION).astype(np.float32).tolist()
        
        try:
            response = self.openai_client.client.embeddings.create(
                model="text-embedding-3-small",
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return None
    
    def save(self):
        """Save the index and documents to disk"""
        logger.info("Saving vector store and document store")
        
        # Save FAISS index
        if self.index is not None:
            faiss.write_index(self.index, VECTOR_STORE_PATH)
        
        # Save document store
        with open(DOCUMENT_STORE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.documents, f, indent=2)
    
    def load(self):
        """Load the index and documents from disk"""
        logger.info("Loading vector store and document store")
        
        # Load FAISS index
        if os.path.exists(VECTOR_STORE_PATH):
            self.index = faiss.read_index(VECTOR_STORE_PATH)
        
        # Load document store
        if os.path.exists(DOCUMENT_STORE_PATH):
            with open(DOCUMENT_STORE_PATH, 'r', encoding='utf-8') as f:
                self.documents = json.load(f)
    
    def query(self, question: str, top_k: int = 5) -> Dict[str, Any]:
        """
        Query the RAG system with a question.
        
        Args:
            question: The question to answer.
            top_k: Number of top documents to retrieve.
            
        Returns:
            Dictionary with answer and sources.
        """
        logger.info(f"Processing query: {question}")
        
        if not self.openai_client:
            return {
                "answer": "OpenAI client not available. Please set OPENAI_API_KEY environment variable.",
                "sources": []
            }
        
        if self.index is None or not self.documents:
            return {
                "answer": "RAG system not initialized. Please run initialize() first.",
                "sources": []
            }
        
        # Get embedding for the question
        question_embedding = self._get_embedding(question)
        if question_embedding is None:
            return {
                "answer": "Failed to generate embedding for the question.",
                "sources": []
            }
        
        # Search for similar documents
        distances, indices = self.index.search(
            np.array([question_embedding], dtype=np.float32), 
            min(top_k, self.index.ntotal)
        )
        
        # Get the retrieved documents
        retrieved_docs = []
        for i, idx in enumerate(indices[0]):
            if idx < 0 or idx >= len(self.documents):
                continue
                
            # Get document ID
            doc_id = list(self.documents.keys())[idx]
            doc = self.documents[doc_id]
            
            retrieved_docs.append({
                "content": doc["content"],
                "source": doc["source"],
                "metadata": doc.get("metadata", {}),
                "distance": float(distances[0][i])
            })
        
        # Generate context from retrieved documents
        context = "\n\n".join([
            f"[Document {i+1} from {doc['source']}]\n{doc['content']}"
            for i, doc in enumerate(retrieved_docs)
        ])
        
        # Generate answer using OpenAI
        prompt = f"""
        Answer the following question based on the provided context. If the answer cannot be found in the context, say "I don't have enough information to answer this question."
        
        Context:
        {context}
        
        Question: {question}
        
        Answer:
        """
        
        try:
            response = self.openai_client.chat_completion(
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions about a code repository based on its documentation and analysis."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            answer = response.choices[0].message.content
            
            # Format sources
            sources = []
            for doc in retrieved_docs:
                source_info = {
                    "source": doc["source"],
                    "metadata": doc["metadata"]
                }
                if source_info not in sources:
                    sources.append(source_info)
            
            return {
                "answer": answer,
                "sources": sources
            }
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            return {
                "answer": f"Error generating answer: {str(e)}",
                "sources": []
            }

def initialize_rag_system(force: bool = False) -> bool:
    """
    Initialize the RAG system.
    
    Args:
        force: If True, reinitialize even if the system is already initialized.
        
    Returns:
        True if initialization was successful, False otherwise.
    """
    try:
        rag = RAGSystem()
        return rag.initialize(force=force)
    except Exception as e:
        logger.exception(f"Error initializing RAG system: {str(e)}")
        return False

def query_rag_system(question: str) -> str:
    """
    Query the RAG system with a question.
    
    Args:
        question: The question to answer.
        
    Returns:
        The answer with source information.
    """
    try:
        rag = RAGSystem()
        rag.load()
        result = rag.query(question)
        
        answer = result["answer"]
        sources = result["sources"]
        
        # Format the response with sources
        if sources:
            source_text = "\n\nSources:\n" + "\n".join([
                f"- {source['source']}" + 
                (f" ({source['metadata'].get('section', '')})" if source['metadata'].get('section') else "")
                for source in sources
            ])
            return answer + source_text
        else:
            return answer
    except Exception as e:
        logger.exception(f"Error querying RAG system: {str(e)}")
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Test the RAG system
    initialize_rag_system(force=True)
    
    test_questions = [
        "What is the primary purpose of this repository?",
        "What are the key strengths of this codebase?",
        "What security issues were identified in the analysis?",
        "How does Mistral's analysis compare to OpenAI's analysis?"
    ]
    
    for question in test_questions:
        print(f"\nQuestion: {question}")
        print("-" * 50)
        print(query_rag_system(question))
        print("=" * 50)

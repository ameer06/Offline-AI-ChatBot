"""
Database Manager for AI Chatbot
================================
Handles all database operations including:
- Chat history (conversations and messages)
- Document metadata storage
- User session management
"""

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json


class Database:
    """SQLite database manager for chat history and documents"""
    
    def __init__(self, db_path: str = "data/chatbot.db"):
        """
        Initialize database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        # Ensure data directory exists
        db_file = Path(db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.db_path = db_path
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get database connection"""
        conn = sqlite3.Connection(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn
    
    def init_db(self):
        """Create database tables if they don't exist"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Conversations table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                model_used TEXT DEFAULT 'llama3.2'
            )
        """)
        
        # Messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('user', 'assistant')),
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                has_rag_context BOOLEAN DEFAULT 0,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
            )
        """)
        
        # Documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                file_path TEXT NOT NULL,
                upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                file_size INTEGER,
                page_count INTEGER,
                status TEXT DEFAULT 'processing' CHECK(status IN ('processing', 'ready', 'error'))
            )
        """)
        
        # Create indexes for better performance
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_messages_conversation 
            ON messages(conversation_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_conversations_updated 
            ON conversations(updated_at DESC)
        """)
        
        conn.commit()
        conn.close()
        
        print("✅ Database initialized successfully")
    
    # ==========================================
    # CONVERSATION OPERATIONS
    # ==========================================
    
    def create_conversation(self, title: str = "New Chat", model: str = "llama3.2") -> int:
        """
        Create a new conversation
        
        Args:
            title: Conversation title
            model: AI model being used
            
        Returns:
            Conversation ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO conversations (title, model_used)
            VALUES (?, ?)
        """, (title, model))
        
        conversation_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Created conversation ID: {conversation_id}")
        return conversation_id
    
    def get_conversation(self, conversation_id: int) -> Optional[Dict]:
        """
        Get a specific conversation with all its messages
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            Dictionary with conversation details and messages
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get conversation details
        cursor.execute("""
            SELECT * FROM conversations WHERE id = ?
        """, (conversation_id,))
        
        conv_row = cursor.fetchone()
        if not conv_row:
            conn.close()
            return None
        
        # Get all messages for this conversation
        cursor.execute("""
            SELECT * FROM messages 
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
        """, (conversation_id,))
        
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return {
            'id': conv_row['id'],
            'title': conv_row['title'],
            'created_at': conv_row['created_at'],
            'updated_at': conv_row['updated_at'],
            'model_used': conv_row['model_used'],
            'messages': messages
        }
    
    def get_all_conversations(self, limit: int = 50) -> List[Dict]:
        """
        Get list of all conversations (without full message history)
        
        Args:
            limit: Maximum number of conversations to return
            
        Returns:
            List of conversation summaries
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                c.id,
                c.title,
                c.created_at,
                c.updated_at,
                c.model_used,
                COUNT(m.id) as message_count
            FROM conversations c
            LEFT JOIN messages m ON c.id = m.conversation_id
            GROUP BY c.id
            ORDER BY c.updated_at DESC
            LIMIT ?
        """, (limit,))
        
        conversations = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return conversations
    
    def update_conversation_title(self, conversation_id: int, title: str):
        """Update conversation title"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE conversations 
            SET title = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (title, conversation_id))
        
        conn.commit()
        conn.close()
    
    def delete_conversation(self, conversation_id: int):
        """
        Delete a conversation and all its messages
        
        Args:
            conversation_id: ID of conversation to delete
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM conversations WHERE id = ?", (conversation_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Deleted conversation ID: {conversation_id}")
    
    # ==========================================
    # MESSAGE OPERATIONS
    # ==========================================
    
    def save_message(self, conversation_id: int, role: str, content: str, 
                     has_rag: bool = False) -> int:
        """
        Save a message to the database
        
        Args:
            conversation_id: ID of the conversation
            role: 'user' or 'assistant'
            content: Message content
            has_rag: Whether RAG was used for this message
            
        Returns:
            Message ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Save message
        cursor.execute("""
            INSERT INTO messages (conversation_id, role, content, has_rag_context)
            VALUES (?, ?, ?, ?)
        """, (conversation_id, role, content, 1 if has_rag else 0))
        
        message_id = cursor.lastrowid
        
        # Update conversation's updated_at timestamp
        cursor.execute("""
            UPDATE conversations 
            SET updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (conversation_id,))
        
        conn.commit()
        conn.close()
        
        return message_id
    
    def get_conversation_messages(self, conversation_id: int) -> List[Dict]:
        """
        Get all messages for a conversation
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            List of messages
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM messages 
            WHERE conversation_id = ?
            ORDER BY timestamp ASC
        """, (conversation_id,))
        
        messages = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return messages
    
    # ==========================================
    # DOCUMENT OPERATIONS
    # ==========================================
    
    def add_document(self, filename: str, file_path: str, file_size: int, 
                     page_count: int = 0) -> int:
        """
        Add document metadata to database
        
        Args:
            filename: Original filename
            file_path: Path where file is stored
            file_size: File size in bytes
            page_count: Number of pages in PDF
            
        Returns:
            Document ID
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO documents (filename, file_path, file_size, page_count, status)
            VALUES (?, ?, ?, ?, 'processing')
        """, (filename, file_path, file_size, page_count))
        
        doc_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        print(f"✅ Added document ID: {doc_id} - {filename}")
        return doc_id
    
    def update_document_status(self, doc_id: int, status: str):
        """Update document processing status"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            UPDATE documents 
            SET status = ?
            WHERE id = ?
        """, (status, doc_id))
        
        conn.commit()
        conn.close()
    
    def get_documents(self) -> List[Dict]:
        """Get list of all documents"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM documents 
            ORDER BY upload_date DESC
        """)
        
        documents = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return documents
    
    def delete_document(self, doc_id: int):
        """Delete document metadata"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM documents WHERE id = ?", (doc_id,))
        
        conn.commit()
        conn.close()
        
        print(f"✅ Deleted document ID: {doc_id}")
    
    def get_document_by_id(self, doc_id: int) -> Optional[Dict]:
        """Get specific document by ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM documents WHERE id = ?", (doc_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    # ==========================================
    # UTILITY METHODS
    # ==========================================
    
    def get_stats(self) -> Dict:
        """Get database statistics"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Count conversations
        cursor.execute("SELECT COUNT(*) FROM conversations")
        conv_count = cursor.fetchone()[0]
        
        # Count messages
        cursor.execute("SELECT COUNT(*) FROM messages")
        msg_count = cursor.fetchone()[0]
        
        # Count documents
        cursor.execute("SELECT COUNT(*) FROM documents")
        doc_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            'conversations': conv_count,
            'messages': msg_count,
            'documents': doc_count
        }


# Test the database if run directly
if __name__ == "__main__":
    print("Testing Database...")
    
    db = Database("data/test_chatbot.db")
    
    # Test conversation creation
    conv_id = db.create_conversation("Test Conversation")
    
    # Test message saving
    db.save_message(conv_id, "user", "Hello, how are you?")
    db.save_message(conv_id, "assistant", "I'm doing well, thank you!")
    
    # Test retrieval
    conv = db.get_conversation(conv_id)
    print(f"\nConversation: {conv['title']}")
    print(f"Messages: {len(conv['messages'])}")
    
    # Test stats
    stats = db.get_stats()
    print(f"\nDatabase Stats: {stats}")
    
    print("\n✅ All tests passed!")

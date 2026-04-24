"""
Database connection and utilities for GenMentor
"""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, Dict, Any, List

class DatabaseManager:
    def __init__(self):
        self.connection_params = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432'),
            'database': os.getenv('DB_NAME', 'genmentor'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', 'password')
        }
    
    @contextmanager
    def get_connection(self):
        """Get database connection with context manager"""
        conn = None
        try:
            conn = psycopg2.connect(**self.connection_params)
            yield conn
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()
    
    def execute_query(self, query: str, params: Optional[tuple] = None, fetch: bool = True) -> Optional[List[Dict[str, Any]]]:
        """Execute a query and return results"""
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, params)
            
            if fetch:
                results = cursor.fetchall()
                return [dict(row) for row in results]
            else:
                conn.commit()
                return None
    
    def get_roles(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all roles, optionally filtered by category"""
        query = "SELECT * FROM roles"
        params = None
        
        if category:
            query += " WHERE category = %s"
            params = (category,)
        
        query += " ORDER BY name"
        return self.execute_query(query, params)
    
    def get_skills(self, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get all skills, optionally filtered by category"""
        query = "SELECT * FROM skills"
        params = None
        
        if category:
            query += " WHERE category = %s"
            params = (category,)
        
        query += " ORDER BY name"
        return self.execute_query(query, params)
    
    def get_role_skill_requirements(self, role_id: int) -> List[Dict[str, Any]]:
        """Get skill requirements for a specific role"""
        query = """
            SELECT s.*, rsr.proficiency_level, rsr.importance
            FROM skills s
            JOIN role_skill_requirements rsr ON s.id = rsr.skill_id
            WHERE rsr.role_id = %s
            ORDER BY rsr.importance DESC, s.name
        """
        return self.execute_query(query, (role_id,))
    
    def get_documents(self, category: Optional[str] = None, file_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get documents, optionally filtered by category or file type"""
        query = "SELECT * FROM documents WHERE 1=1"
        params = []
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        if file_type:
            query += " AND file_type = %s"
            params.append(file_type)
        
        query += " ORDER BY created_at DESC"
        return self.execute_query(query, tuple(params) if params else None)
    
    def search_documents(self, search_term: str, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Search documents by title or tags"""
        query = """
            SELECT * FROM documents 
            WHERE (title ILIKE %s OR %s = ANY(tags))
        """
        params = [f"%{search_term}%", search_term]
        
        if category:
            query += " AND category = %s"
            params.append(category)
        
        query += " ORDER BY created_at DESC"
        return self.execute_query(query, tuple(params))
    
    def create_learner(self, email: str, name: str, profile: Dict[str, Any]) -> int:
        """Create a new learner"""
        query = """
            INSERT INTO learners (email, name, profile)
            VALUES (%s, %s, %s)
            ON CONFLICT (email) DO UPDATE SET
                name = EXCLUDED.name,
                profile = EXCLUDED.profile,
                updated_at = CURRENT_TIMESTAMP
            RETURNING id
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (email, name, psycopg2.extras.Json(profile)))
            learner_id = cursor.fetchone()['id']
            conn.commit()
            return learner_id
    
    def get_learner(self, learner_id: int) -> Optional[Dict[str, Any]]:
        """Get learner by ID"""
        query = "SELECT * FROM learners WHERE id = %s"
        results = self.execute_query(query, (learner_id,))
        return results[0] if results else None
    
    def create_learning_path(self, learner_id: int, name: str, description: str, 
                           target_role_id: Optional[int] = None, sessions: List[Dict[str, Any]] = None) -> int:
        """Create a new learning path"""
        query = """
            INSERT INTO learning_paths (learner_id, name, description, target_role_id, sessions)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute(query, (
                learner_id, name, description, target_role_id, 
                psycopg2.extras.Json(sessions or [])
            ))
            path_id = cursor.fetchone()['id']
            conn.commit()
            return path_id
    
    def get_learning_path(self, path_id: int) -> Optional[Dict[str, Any]]:
        """Get learning path by ID"""
        query = "SELECT * FROM learning_paths WHERE id = %s"
        results = self.execute_query(query, (path_id,))
        return results[0] if results else None
    
    def update_learning_path_progress(self, path_id: int, progress: Dict[str, Any]):
        """Update learning path progress"""
        query = """
            UPDATE learning_paths 
            SET progress = %s, updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """
        self.execute_query(query, (psycopg2.extras.Json(progress), path_id), fetch=False)

# Global database manager instance
db_manager = DatabaseManager()
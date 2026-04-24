#!/usr/bin/env python3
"""
Database setup script for GenMentor MVP
Creates database schema and initial data
"""

import os
import sys
import json
import psycopg2
from psycopg2.extras import RealDictCursor
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent))

def get_db_connection():
    """Get database connection from environment variables"""
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

def create_database_if_not_exists():
    """Create database if it doesn't exist"""
    try:
        # Connect to default postgres database
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database='postgres',
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', 'password')
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        db_name = os.getenv('DB_NAME', 'genmentor')
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"Database '{db_name}' created successfully")
        else:
            print(f"Database '{db_name}' already exists")
            
        cursor.close()
        conn.close()
        
    except psycopg2.Error as e:
        print(f"Error creating database: {e}")
        return False
    
    return True

def run_schema_script():
    """Run the database schema script"""
    schema_path = Path(__file__).parent.parent.parent / "seed_data" / "database" / "minimal_schema.sql"
    
    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}")
        return False
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor()
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        cursor.execute(schema_sql)
        conn.commit()
        print("Database schema created successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except psycopg2.Error as e:
        print(f"Error running schema script: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def seed_taxonomy_data():
    """Seed taxonomy data from JSON files"""
    taxonomy_path = Path(__file__).parent.parent.parent / "seed_data" / "taxonomy"
    
    if not taxonomy_path.exists():
        print(f"Taxonomy directory not found: {taxonomy_path}")
        return False
    
    conn = get_db_connection()
    if not conn:
        return False
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Load roles
        roles_file = taxonomy_path / "roles.json"
        if roles_file.exists():
            with open(roles_file, 'r', encoding='utf-8') as f:
                roles_data = json.load(f)
            
            for role in roles_data:
                cursor.execute("""
                    INSERT INTO roles (name, description, category, level)
                    VALUES (%(name)s, %(description)s, %(category)s, %(level)s)
                    ON CONFLICT (name) DO UPDATE SET
                        description = EXCLUDED.description,
                        category = EXCLUDED.category,
                        level = EXCLUDED.level
                    RETURNING id
                """, role)
                role_id = cursor.fetchone()['id']
                print(f"Inserted/Updated role: {role['name']} (ID: {role_id})")
        
        # Load skills
        skills_file = taxonomy_path / "skills.json"
        if skills_file.exists():
            with open(skills_file, 'r', encoding='utf-8') as f:
                skills_data = json.load(f)
            
            for skill in skills_data:
                cursor.execute("""
                    INSERT INTO skills (name, description, category, level)
                    VALUES (%(name)s, %(description)s, %(category)s, %(level)s)
                    ON CONFLICT (name) DO UPDATE SET
                        description = EXCLUDED.description,
                        category = EXCLUDED.category,
                        level = EXCLUDED.level
                    RETURNING id
                """, skill)
                skill_id = cursor.fetchone()['id']
                print(f"Inserted/Updated skill: {skill['name']} (ID: {skill_id})")
        
        # Create role-skill mappings
        cursor.execute("SELECT id, name FROM roles")
        roles_map = {row['name']: row['id'] for row in cursor.fetchall()}
        
        cursor.execute("SELECT id, name FROM skills")
        skills_map = {row['name']: row['id'] for row in cursor.fetchall()}
        
        # Map roles to skills based on taxonomy data
        with open(roles_file, 'r', encoding='utf-8') as f:
            roles_data = json.load(f)
        
        for role in roles_data:
            role_id = roles_map.get(role['name'])
            if role_id and 'required_skills' in role:
                for skill_name in role['required_skills']:
                    skill_id = skills_map.get(skill_name)
                    if skill_id:
                        cursor.execute("""
                            INSERT INTO role_skill_requirements (role_id, skill_id, proficiency_level, importance)
                            VALUES (%s, %s, %s, %s)
                            ON CONFLICT (role_id, skill_id) DO NOTHING
                        """, (role_id, skill_id, 'intermediate', 'high'))
        
        conn.commit()
        print("Taxonomy data seeded successfully")
        
        cursor.close()
        conn.close()
        return True
        
    except (psycopg2.Error, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error seeding taxonomy data: {e}")
        if conn:
            conn.rollback()
            conn.close()
        return False

def main():
    """Main setup function"""
    print("Starting GenMentor database setup...")
    
    # Check environment variables
    required_env_vars = ['DB_HOST', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("Warning: Missing environment variables:", missing_vars)
        print("Using default values. Make sure to set these in production:")
        print("DB_HOST=localhost")
        print("DB_PORT=5432")
        print("DB_NAME=genmentor")
        print("DB_USER=postgres")
        print("DB_PASSWORD=password")
    
    # Step 1: Create database
    if not create_database_if_not_exists():
        print("Failed to create database")
        return False
    
    # Step 2: Run schema script
    if not run_schema_script():
        print("Failed to create database schema")
        return False
    
    # Step 3: Seed taxonomy data
    if not seed_taxonomy_data():
        print("Failed to seed taxonomy data")
        return False
    
    print("Database setup completed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
-- GenMentor MVP Database Schema
-- Minimal schema for demo purposes

-- Core taxonomy tables
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    category VARCHAR(50),
    level VARCHAR(20) DEFAULT 'intermediate',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS skills (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    category VARCHAR(50),
    level VARCHAR(20) DEFAULT 'beginner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS courses (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    category VARCHAR(50),
    duration_hours INTEGER DEFAULT 0,
    difficulty_level VARCHAR(20) DEFAULT 'beginner',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Mapping tables
CREATE TABLE IF NOT EXISTS role_skill_requirements (
    id SERIAL PRIMARY KEY,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    proficiency_level VARCHAR(20) DEFAULT 'intermediate',
    importance VARCHAR(20) DEFAULT 'medium',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(role_id, skill_id)
);

CREATE TABLE IF NOT EXISTS course_skill_mappings (
    id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES courses(id) ON DELETE CASCADE,
    skill_id INTEGER REFERENCES skills(id) ON DELETE CASCADE,
    skill_coverage VARCHAR(20) DEFAULT 'partial',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(course_id, skill_id)
);

-- Document management
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    title VARCHAR(500),
    file_type VARCHAR(10) NOT NULL,
    file_path VARCHAR(1000) NOT NULL,
    file_size INTEGER DEFAULT 0,
    content_type VARCHAR(50),
    category VARCHAR(100),
    subcategory VARCHAR(100),
    tags TEXT[], -- PostgreSQL array
    metadata JSONB DEFAULT '{}',
    indexed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Assessment system
CREATE TABLE IF NOT EXISTS assessment_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    format VARCHAR(50), -- 'multiple_choice', 'true_false', 'short_answer', 'essay'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS question_bank (
    id SERIAL PRIMARY KEY,
    question_text TEXT NOT NULL,
    question_type VARCHAR(50) NOT NULL,
    skill_id INTEGER REFERENCES skills(id),
    difficulty_level VARCHAR(20) DEFAULT 'medium',
    correct_answer TEXT,
    options JSONB DEFAULT '[]', -- For multiple choice
    explanation TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Learner management
CREATE TABLE IF NOT EXISTS learners (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    name VARCHAR(200),
    profile JSONB DEFAULT '{}',
    current_skills JSONB DEFAULT '[]',
    learning_goals JSONB DEFAULT '[]',
    preferences JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learning_paths (
    id SERIAL PRIMARY KEY,
    learner_id INTEGER REFERENCES learners(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    target_role_id INTEGER REFERENCES roles(id),
    sessions JSONB DEFAULT '[]',
    progress JSONB DEFAULT '{}',
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS learning_sessions (
    id SERIAL PRIMARY KEY,
    learning_path_id INTEGER REFERENCES learning_paths(id) ON DELETE CASCADE,
    session_number INTEGER NOT NULL,
    title VARCHAR(200) NOT NULL,
    content JSONB DEFAULT '{}',
    quiz_data JSONB DEFAULT '{}',
    completed_at TIMESTAMP,
    score DECIMAL(5,2),
    feedback TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_documents_category ON documents(category);
CREATE INDEX IF NOT EXISTS idx_documents_file_type ON documents(file_type);
CREATE INDEX IF NOT EXISTS idx_documents_tags ON documents USING GIN(tags);
CREATE INDEX IF NOT EXISTS idx_documents_metadata ON documents USING GIN(metadata);
CREATE INDEX IF NOT EXISTS idx_question_bank_skill ON question_bank(skill_id);
CREATE INDEX IF NOT EXISTS idx_question_bank_difficulty ON question_bank(difficulty_level);
CREATE INDEX IF NOT EXISTS idx_learners_email ON learners(email);
CREATE INDEX IF NOT EXISTS idx_learning_paths_learner ON learning_paths(learner_id);
CREATE INDEX IF NOT EXISTS idx_learning_sessions_path ON learning_sessions(learning_path_id);

-- Sample data inserts
INSERT INTO roles (name, description, category, level) VALUES
('AI Engineer', 'Develops and implements AI/ML solutions', 'Technology', 'advanced'),
('Data Scientist', 'Analyzes data to extract business insights', 'Analytics', 'intermediate'),
('Software Developer', 'Builds software applications and systems', 'Technology', 'intermediate'),
('ERP Consultant', 'Implements and configures ERP systems', 'Business', 'intermediate'),
('Business Analyst', 'Analyzes business processes and requirements', 'Business', 'beginner')
ON CONFLICT (name) DO NOTHING;

INSERT INTO skills (name, description, category, level) VALUES
('Python Programming', 'Programming in Python language', 'Programming', 'beginner'),
('Machine Learning', 'Understanding ML algorithms and applications', 'AI/ML', 'intermediate'),
('Data Analysis', 'Analyzing and interpreting data', 'Analytics', 'beginner'),
('SQL', 'Database querying and management', 'Database', 'beginner'),
('Deep Learning', 'Neural networks and deep learning', 'AI/ML', 'advanced'),
('ERP Configuration', 'Configuring ERP systems', 'Business Systems', 'intermediate'),
('Process Modeling', 'Business process analysis and modeling', 'Business', 'intermediate'),
('API Development', 'Building REST APIs', 'Programming', 'intermediate'),
('Data Visualization', 'Creating charts and dashboards', 'Analytics', 'beginner'),
('Project Management', 'Managing software projects', 'Management', 'intermediate')
ON CONFLICT (name) DO NOTHING;

INSERT INTO assessment_types (name, description, format) VALUES
('Multiple Choice', 'Questions with multiple options', 'multiple_choice'),
('True/False', 'Binary choice questions', 'true_false'),
('Short Answer', 'Brief text responses', 'short_answer'),
('Essay', 'Long form written responses', 'essay'),
('Practical Exercise', 'Hands-on coding or implementation', 'practical')
ON CONFLICT (name) DO NOTHING;
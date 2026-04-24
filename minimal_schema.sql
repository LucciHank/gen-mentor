CREATE TABLE documents (
  document_id VARCHAR(20) PRIMARY KEY,
  title TEXT NOT NULL,
  file_name TEXT NOT NULL,
  source_uri TEXT NOT NULL,
  file_type VARCHAR(10) NOT NULL,
  topic VARCHAR(50) NOT NULL,
  content_type VARCHAR(50) NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'draft',
  can_use_for_generation BOOLEAN NOT NULL DEFAULT FALSE,
  can_use_for_assessment BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE document_chunks (
  chunk_id BIGSERIAL PRIMARY KEY,
  document_id VARCHAR(20) NOT NULL REFERENCES documents(document_id),
  section_title TEXT,
  chunk_text TEXT NOT NULL,
  chunk_order INT NOT NULL,
  token_count INT,
  metadata_json JSONB,
  embedding VECTOR(768)
);

CREATE TABLE roles (
  role_id VARCHAR(40) PRIMARY KEY,
  role_name TEXT NOT NULL,
  department TEXT,
  description TEXT
);

CREATE TABLE skills (
  skill_id VARCHAR(40) PRIMARY KEY,
  skill_name TEXT NOT NULL,
  domain TEXT,
  description TEXT
);

CREATE TABLE role_skill_requirements (
  role_id VARCHAR(40) NOT NULL REFERENCES roles(role_id),
  skill_id VARCHAR(40) NOT NULL REFERENCES skills(skill_id),
  required_level VARCHAR(20) NOT NULL,
  importance_weight INT NOT NULL,
  PRIMARY KEY (role_id, skill_id)
);

CREATE TABLE courses (
  course_id VARCHAR(20) PRIMARY KEY,
  course_name TEXT NOT NULL,
  track TEXT,
  description TEXT
);

CREATE TABLE lessons (
  lesson_id VARCHAR(20) PRIMARY KEY,
  course_id VARCHAR(20) NOT NULL REFERENCES courses(course_id),
  module_id VARCHAR(20),
  lesson_name TEXT NOT NULL,
  skill_id VARCHAR(40) REFERENCES skills(skill_id),
  level_target VARCHAR(20),
  duration_minutes INT,
  prerequisite_ids TEXT,
  source_tags TEXT
);

CREATE TABLE assessment_items (
  item_id VARCHAR(20) PRIMARY KEY,
  skill_id VARCHAR(40) NOT NULL REFERENCES skills(skill_id),
  level VARCHAR(20) NOT NULL,
  question_type VARCHAR(20) NOT NULL,
  question_stem TEXT NOT NULL,
  options_json JSONB,
  expected_answer_json JSONB,
  rubric_json JSONB,
  status VARCHAR(20) NOT NULL DEFAULT 'approved'
);

CREATE TABLE learners (
  learner_id BIGSERIAL PRIMARY KEY,
  full_name TEXT,
  email TEXT,
  target_role_id VARCHAR(40) REFERENCES roles(role_id),
  goal_text TEXT,
  current_status VARCHAR(20) DEFAULT 'new'
);

CREATE TABLE learner_diagnostic_results (
  result_id BIGSERIAL PRIMARY KEY,
  learner_id BIGINT NOT NULL REFERENCES learners(learner_id),
  skill_id VARCHAR(40) NOT NULL REFERENCES skills(skill_id),
  score NUMERIC(5,2) NOT NULL,
  inferred_level VARCHAR(20) NOT NULL,
  evidence_json JSONB,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE learning_paths (
  path_id BIGSERIAL PRIMARY KEY,
  learner_id BIGINT NOT NULL REFERENCES learners(learner_id),
  target_role_id VARCHAR(40) REFERENCES roles(role_id),
  version_no INT NOT NULL DEFAULT 1,
  path_status VARCHAR(20) NOT NULL DEFAULT 'draft',
  summary_json JSONB,
  created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE learning_path_nodes (
  node_id BIGSERIAL PRIMARY KEY,
  path_id BIGINT NOT NULL REFERENCES learning_paths(path_id),
  week_no INT NOT NULL,
  lesson_id VARCHAR(20) REFERENCES lessons(lesson_id),
  objective TEXT,
  estimated_minutes INT,
  node_order INT NOT NULL
);
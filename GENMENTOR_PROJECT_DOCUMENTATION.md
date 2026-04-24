# GENMENTOR - Tài Liệu Dự Án Hoàn Chỉnh

## 📋 Tổng Quan Dự Án

**GenMentor** là một nền tảng học tập cá nhân hóa được hỗ trợ bởi AI, tạo ra trải nghiệm học tập thích ứng được điều chỉnh theo nhu cầu, khoảng cách kỹ năng và mục tiêu của từng người học.

### 🎯 Mục Tiêu Chính
- Phân tích khoảng cách kỹ năng cá nhân
- Tạo lộ trình học tập thích ứng
- Cung cấp nội dung học tập được cá nhân hóa
- Hỗ trợ học tập tương tác với AI Tutor
- Theo dõi và cập nhật hồ sơ người học

---

## 🏗️ Kiến Trúc Hệ Thống

### Stack Công Nghệ

**Backend (FastAPI + Python 3.12+)**
- **Framework**: FastAPI cho REST API
- **AI Orchestration**: LangChain/LangGraph
- **LLM Providers**: DeepSeek (mặc định), OpenAI, Anthropic, Ollama
- **Vector Database**: ChromaDB cho RAG
- **Search**: DuckDuckGo Web Search
- **Embeddings**: Sentence Transformers
- **Configuration**: Hydra với YAML

**Frontend (Streamlit)**
- **UI Framework**: Streamlit
- **State Management**: Session state + JSON persistence
- **HTTP Client**: httpx cho API calls
- **Document Processing**: pdfplumber, markdown

### Cấu Trúc Thư Mục

```
gen-mentor/
├── backend/                    # FastAPI backend service
│   ├── main.py                # Entry point, API routes
│   ├── api_schemas.py         # Pydantic request/response models
│   ├── requirements.txt       # Python dependencies
│   │
│   ├── config/                # Hydra configuration system
│   │   ├── main.yaml         # Main app config
│   │   ├── default.yaml      # Default module settings
│   │   ├── loader.py         # Config loading utilities
│   │   └── schemas.py        # Config validation schemas
│   │
│   ├── base/                  # Core components và factories
│   │   ├── base_agent.py     # BaseAgent class cho tất cả agents
│   │   ├── llm_factory.py    # LLM provider factory
│   │   ├── rag_factory.py    # RAG system factory
│   │   ├── embedder_factory.py # Embedding model factory
│   │   ├── searcher_factory.py # Search provider factory
│   │   └── search_rag.py     # Search + RAG integration
│   │
│   ├── modules/               # Feature modules (agent-based)
│   │   ├── ai_chatbot_tutor/
│   │   ├── skill_gap_identification/
│   │   ├── adaptive_learner_modeling/
│   │   ├── personalized_resource_delivery/
│   │   └── learner_simulation/
│   │
│   ├── utils/                 # Shared utilities
│   │   ├── config.py         # Config helpers
│   │   ├── llm_output.py     # LLM response processing
│   │   └── preprocess.py     # Document preprocessing
│   │
│   └── data/                  # Runtime data
│       └── vectorstore/      # ChromaDB storage
│
├── frontend/                   # Streamlit UI application
│   ├── main.py               # Entry point, navigation
│   ├── config.py             # Frontend config
│   ├── requirements.txt      # Python dependencies
│   ├── data_store.json       # Persistent UI state
│   │
│   ├── .streamlit/
│   │   └── config.toml       # Streamlit theme/layout
│   │
│   ├── assets/               # UI resources
│   │   ├── css/             # UI styles
│   │   └── data_example/    # Mock data cho offline mode
│   │
│   ├── components/           # Reusable UI components
│   │   ├── chatbot/         # Chat interface
│   │   └── time_tracking/   # Session timing
│   │
│   ├── pages/                # Multi-page app screens
│   │   ├── onboarding.py    # Learner info collection
│   │   ├── goal_management.py # Goal refinement
│   │   ├── learning_path.py # Path scheduling/navigation
│   │   ├── knowledge_document.py # In-session reading
│   │   └── dashboard.py     # Analytics overview
│   │
│   └── utils/                # Frontend utilities
│       ├── request_api.py   # Backend API client
│       ├── state.py         # State management
│       ├── formatting.py    # Display helpers
│       └── colors.py        # Theme colors
│
└── .kiro/                     # Kiro AI assistant configuration
```

---

## 🤖 Kiến Trúc AI Agent

### Base Agent Pattern

Tất cả AI agents kế thừa từ `BaseAgent` với:

```python
class BaseAgent:
    def __init__(self, model, system_prompt, tools=None, **kwargs):
        # Khởi tạo với LLM instance + system prompt
        
    def invoke(self, input_dict, task_prompt):
        # Gọi LLM với retry logic
        # Trả về JSON được validate
```

**Workflow Pattern**:
1. **Payload Validation**: Pydantic models validate input
2. **Task Prompt Formatting**: Template với {variables}
3. **LLM Invocation**: Với exponential backoff retry (1-10s)
4. **Output Schema Validation**: Pydantic validation
5. **Return Structured Data**: JSON format

---

## 🧩 5 Module Chính

### 1. 🎯 Skill Gap Identification

**Mục đích**: Phân tích khoảng cách kỹ năng giữa hiện tại và mục tiêu

**Agents**:
- **`SkillRequirementMapper`**: Ánh xạ mục tiêu học tập → kỹ năng cần thiết (1-10 skills)
- **`SkillGapIdentifier`**: Phân tích thông tin người học so với yêu cầu
- **`LearningGoalRefiner`**: Làm rõ mục tiêu mơ hồ

**Input**: Learning goal + learner information (CV, occupation, experience)
**Output**: Structured skill gaps với proficiency levels (unlearned/beginner/intermediate/advanced)

**API Endpoints**:
- `POST /refine-learning-goal` → refined goal
- `POST /identify-skill-gap-with-info` → skill gaps + requirements
- `POST /identify-skill-gap` → CV upload version

### 2. 👤 Adaptive Learner Modeling

**Mục đích**: Tạo và cập nhật hồ sơ người học thích ứng

**Agent**:
- **`AdaptiveLearnerProfiler`**: Tạo/cập nhật learner profiles

**Learner Profile Structure**:
```json
{
  "learner_information": "string",
  "learning_goal": "string",
  "cognitive_status": {
    "overall_progress": "0-100%",
    "mastered_skills": [{"name": "skill", "proficiency_level": "advanced"}],
    "in_progress_skills": [{"name": "skill", "required_level": "intermediate", "current_level": "beginner"}]
  },
  "learning_preferences": {
    "content_style": "visual/textual/interactive",
    "activity_type": "reading/practice/discussion",
    "additional_notes": "string"
  },
  "behavioral_patterns": {
    "system_usage_frequency": "daily/weekly/occasional",
    "session_duration_engagement": "short/medium/long",
    "motivational_triggers": "achievement/progress/social",
    "additional_notes": "string"
  }
}
```

**API Endpoints**:
- `POST /create-learner-profile-with-info` → learner profile
- `POST /update-learner-profile` → updated profile

### 3. 📚 Personalized Resource Delivery

**Mục đích**: Tạo nội dung học tập được cá nhân hóa

**7 Agents**:
- **`LearningPathScheduler`**: Tạo chuỗi học tập 1-10 sessions
- **`GoalOrientedKnowledgeExplorer`**: Xác định knowledge points (foundational/practical/strategic)
- **`SearchEnhancedKnowledgeDrafter`**: Tạo nội dung với RAG (web search + vector retrieval)
- **`LearningDocumentIntegrator`**: Kết hợp drafts thành markdown documents
- **`DocumentQuizGenerator`**: Tạo 4 loại quiz (single-choice, multiple-choice, true/false, short-answer)
- **`LearningContentCreator`**: Điều phối toàn bộ content pipeline
- **`LearnerFeedbackSimulator`**: Mô phỏng phản hồi người học

**Content Generation Pipeline** (4 stages):
```
Stage 1: GoalOrientedKnowledgeExplorer → knowledge_points[]
Stage 2: SearchEnhancedKnowledgeDrafter → knowledge_drafts[] (parallel processing)
Stage 3: LearningDocumentIntegrator → markdown document
Stage 4: DocumentQuizGenerator → quizzes
```

**API Endpoints**:
- `POST /schedule-learning-path` → learning path (1-10 sessions)
- `POST /reschedule-learning-path` → rescheduled path
- `POST /explore-knowledge-points` → knowledge points
- `POST /draft-knowledge-point` → single draft
- `POST /draft-knowledge-points` → parallel drafts
- `POST /integrate-learning-document` → markdown document
- `POST /generate-document-quizzes` → quiz questions
- `POST /tailor-knowledge-content` → full content pipeline

### 4. 💬 AI Chatbot Tutor

**Mục đích**: Hỗ trợ học tập tương tác qua chat

**Agent**:
- **`AITutorChatbot`**: Conversational tutoring với RAG context

**Features**:
- Message history support
- Learner profile context
- Web search + vectorstore retrieval
- Vietnamese responses với personalized guidance

**API Endpoint**:
- `POST /chat-with-tutor` → tutor response

### 5. 🧪 Learner Simulation

**Mục đích**: Mô phỏng và test hành vi người học

**Agents**:
- **`GroundTruthProfileCreator`**: Tạo synthetic learner profiles cho testing
- **`LearnerInteractionSimulator`**: Mô phỏng hành vi người học qua sessions

---

## 🔄 Luồng Hoạt động Chi Tiết

### 1. User Journey Flow

```
[ONBOARDING] 
    ↓
Collect: Learning Goal + Learner Info (occupation, CV, preferences)
    ↓
[SKILL GAP ANALYSIS]
    ↓ 
API: /refine-learning-goal → refined goal
API: /identify-skill-gap-with-info → skill gaps + requirements
    ↓
[LEARNER PROFILE CREATION]
    ↓
API: /create-learner-profile-with-info → learner profile
    ↓
[LEARNING PATH GENERATION]
    ↓
API: /schedule-learning-path → 1-10 sessions learning path
    ↓
[SESSION CONTENT GENERATION] (per session)
    ↓
API: /tailor-knowledge-content → 4-stage pipeline:
  Stage 1: Explore knowledge points
  Stage 2: Draft content (parallel processing)
  Stage 3: Integrate document
  Stage 4: Generate quizzes
    ↓
[IN-SESSION LEARNING]
    ↓
- Read generated content (section by section)
- Take quizzes (4 types)
- Chat with AI Tutor (optional)
- Provide feedback (clarity, relevance, depth, engagement)
    ↓
[PROFILE UPDATE]
    ↓
API: /update-learner-profile → updated profile based on:
  - Learner interactions (quiz performance, feedback)
  - Session information (completed skills)
  - Behavioral observations
    ↓
[PATH RESCHEDULING] (optional)
    ↓
API: /reschedule-learning-path → adjusted path based on updated profile
```

### 2. Technical Data Flow

```
FRONTEND (Streamlit)
    ↓ HTTP Request
BACKEND (FastAPI)
    ↓ Load Config
LLM Factory → Get LLM Instance
    ↓ Instantiate Agent
Agent → Invoke with Prompt
    ↓ Call LLM
LLM → Process Response
    ↓ Validate Output
Pydantic Schema → Return JSON
    ↓ HTTP Response
FRONTEND → Render UI
```

### 3. Content Generation Deep Dive

**Knowledge Point Exploration**:
```python
Input: {learner_profile, learning_path, learning_session}
Process: LLM identifies 3-5 knowledge points per session
Output: Points categorized as foundational/practical/strategic
```

**Content Drafting Pipeline** (Parallel Processing):
```python
# ThreadPoolExecutor, max_workers=3
for knowledge_point in knowledge_points:
    1. Query construction: session_title + knowledge_point_name
    2. Web search + vectorstore retrieval
    3. Format context for LLM
    4. Generate draft with title + content
    5. Error handling per draft (doesn't block others)
```

**Document Integration**:
```python
Input: Multiple knowledge drafts
Process: Combine into cohesive markdown
Output: Sections organized by knowledge point type + overview + summary
```

**Quiz Generation**:
```python
Input: Learning document
Process: Analyze content + generate configurable counts
Output: 
  - Single-choice (default 3)
  - Multiple-choice (default 0) 
  - True/false (default 0)
  - Short-answer (default 0)
Each question includes explanation
```

---

## 🔧 Hệ Thống Cấu Hình

### Configuration Hierarchy (Hydra)

```
default.yaml (base settings)
    ↓
main.yaml (environment overrides)  
    ↓
CLI arguments (highest priority)
```

### Key Configuration Sections

**LLM Configuration**:
```yaml
llm:
  provider: deepseek  # deepseek/openai/anthropic/ollama
  model_name: deepseek-chat
  base_url: null      # Custom base URL
  temperature: 0      # Response randomness (0-1)
```

**Embedding Configuration**:
```yaml
embedding:
  provider: huggingface
  model_name: sentence-transformers/all-mpnet-base-v2
```

**Search & RAG Configuration**:
```yaml
search:
  provider: duckduckgo  # duckduckgo/serper/google
  max_results: 5

vectorstore:
  persist_directory: data/vectorstore
  collection_name: genmentor

rag:
  chunk_size: 1000          # Text chunk size
  num_retrieval_results: 5  # Number of chunks to retrieve
  allow_parallel: true      # Enable parallel processing
  max_workers: 3           # Maximum parallel workers
```

### Environment Variables

```bash
# API Keys (set in .env)
DEEPSEEK_API_KEY=your-deepseek-api-key
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
OLLAMA_BASE_URL=http://localhost:11434

# Search APIs
SERPER_API_KEY=your-serper-key
BING_SUBSCRIPTION_KEY=your-bing-key
BRAVE_API_KEY=your-brave-key
```

---

## 🔍 Search & RAG Integration

### SearchRagManager Architecture

**Components**:
1. **Web Search**: DuckDuckGo → SearchRunner → Document extraction
2. **Vector Storage**: ChromaDB với Sentence Transformers embeddings  
3. **Retrieval Pipeline**:
   - Search query → web results
   - Extract documents → split into chunks (1000 tokens)
   - Add to vectorstore
   - Similarity search (k=5 results)
   - Format for LLM context

**Usage**:
- Knowledge drafting (enriches content với external sources)
- AI tutor (provides context cho responses)
- Optional per-endpoint (use_search flag)

**Performance Optimizations**:
- Parallel processing với ThreadPoolExecutor
- Caching generated documents per session
- Lazy loading components
- 1000-token chunks cho efficiency

---

## 📱 Frontend Pages & Components

### Page Structure

1. **Onboarding** (`pages/onboarding.py`):
   - Step 1: Enter learning goal + goal refinement
   - Step 2: Select occupation + upload CV/info
   - Saves to session_state, persists to data_store.json

2. **Skill Gap** (`pages/skill_gap.py`):
   - Calls `/identify-skill-gap-with-info`
   - Displays identified gaps với proficiency levels

3. **Learning Path** (`pages/learning_path.py`):
   - Displays 1-10 sessions với progress tracking
   - Allows session rescheduling
   - Shows skill mastery rate over time

4. **Knowledge Document** (`pages/knowledge_document.py`):
   - 4-stage content generation với progress indicators
   - Section-by-section pagination với sidebar TOC
   - Auto-scroll to anchors
   - Quiz rendering (4 types)
   - Feedback form (clarity, relevance, depth, engagement)
   - Session completion triggers profile update

5. **Learner Profile** (`pages/learner_profile.py`):
   - Displays current cognitive status
   - Shows mastered vs in-progress skills

6. **Goal Management** (`pages/goal_management.py`):
   - Manage multiple learning goals
   - Refine existing goals

7. **Dashboard** (`pages/dashboard.py`):
   - Analytics overview
   - Learning progress visualization

### State Management

**Frontend State** (`utils/state.py`):
```python
PERSIST_KEYS = [
    "goals", "learner_information", "learner_profile", 
    "learning_path", "document_caches", "session_learning_times",
    "selected_goal_id", "selected_session_id", "if_complete_onboarding"
    # ... 20+ keys total
]
```

- **Session State**: Streamlit session_state
- **Persistence**: JSON file (data_store.json) với whitelisted keys
- **Auto-save**: On page changes
- **Backup**: On reset

**Backend State**:
- **Stateless**: Each request independent
- **LLM Factory**: Caches models per request
- **SearchRagManager**: Singleton per app instance

---

## 🎯 Learning Personalization Mechanism

### Adaptive Profile Components

**Personalization Points**:
1. **Content Adaptation**: Knowledge points selected based on learner level + goal
2. **Difficulty Scaling**: Proficiency levels guide content depth
3. **Learning Preferences**: Content style + activity type influence drafting
4. **Behavioral Tracking**: Session duration, engagement patterns inform rescheduling
5. **Profile Updates**: After each session, profile updated với:
   - Learner interactions (quiz performance, feedback)
   - Session information (completed skills)
   - Behavioral observations
   - Motivational triggers

### Feedback Loop

```
Session Completion 
    ↓
Collect Feedback (clarity, relevance, depth, engagement)
    ↓
Update Learner Profile với feedback
    ↓
Adjust Future Content based on updated profile
    ↓
Reschedule Learning Path (if needed)
```

---

## ⚡ Performance & Resilience

### Error Handling

- **Retry Logic**: Exponential backoff cho transient LLM errors
- **Validation**: Pydantic schemas validate tất cả LLM outputs
- **Graceful Degradation**:
  - Search failures don't block content generation
  - Parallel draft failures logged but don't stop pipeline
  - Mock data fallback trong frontend (use_mock_data flag)
- **Logging**: Structured logging at module level

### Performance Optimizations

- **Parallel Processing**: Knowledge point drafting uses ThreadPoolExecutor
- **Caching**: Frontend caches generated documents per session
- **Lazy Loading**: Components load on demand
- **Streaming**: Long operations show progress indicators
- **Chunking**: RAG uses 1000-token chunks cho efficiency

---

## 🚀 Deployment & Development

### Running the Project

**Backend Setup**:
```bash
cd backend
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 5000
```

**Frontend Setup**:
```bash
cd frontend  
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Start Streamlit UI
streamlit run main.py
```

**Access URLs**:
- Backend API: `http://localhost:5000`
- API Documentation: `http://localhost:5000/docs`
- Frontend UI: `http://localhost:8501`

### Development Workflow

1. **Adding New Features**:
   - Create module under `backend/modules/`
   - Define schemas trong `schemas.py`
   - Implement agents trong `agents/`
   - Add prompts trong `prompts/`
   - Register endpoints trong `main.py`
   - Update API schemas trong `api_schemas.py`

2. **Frontend Development**:
   - Create page trong `pages/`
   - Add API call trong `utils/request_api.py`
   - Update navigation trong `main.py`
   - Add mock data trong `assets/data_example/`

### Configuration Flexibility

- **Multi-Provider Support**: Switch LLM providers via config
- **Environment Overrides**: API keys via .env files
- **Mock Mode**: Frontend can run without backend
- **Custom Base URLs**: Support cho local/custom LLM endpoints
- **Configurable Search**: Toggle web search vs vectorstore-only

---

## 📊 Key Metrics & Analytics

### Learning Analytics

- **Progress Tracking**: Session completion rates, skill mastery progression
- **Engagement Metrics**: Session duration, quiz performance, feedback scores
- **Personalization Effectiveness**: Content relevance ratings, learning path adjustments
- **System Usage**: Feature utilization, error rates, response times

### Performance Metrics

- **API Response Times**: Per endpoint latency monitoring
- **LLM Usage**: Token consumption, model performance comparison
- **Search & RAG**: Query success rates, retrieval relevance
- **User Experience**: Page load times, interaction flows

---

## 🔮 Future Enhancements

### Planned Features

1. **Advanced Analytics Dashboard**: Detailed learning progress visualization
2. **Multi-language Support**: Expand beyond Vietnamese
3. **Collaborative Learning**: Group sessions, peer interactions
4. **Mobile App**: Native mobile experience
5. **Integration APIs**: Connect với external learning platforms
6. **Advanced RAG**: Multi-modal content (images, videos)
7. **Real-time Collaboration**: Live tutoring sessions
8. **Gamification**: Achievement systems, leaderboards

### Technical Improvements

1. **Microservices Architecture**: Split modules into separate services
2. **Kubernetes Deployment**: Container orchestration
3. **Advanced Caching**: Redis integration
4. **Real-time Updates**: WebSocket support
5. **Advanced Security**: OAuth2, rate limiting
6. **Monitoring**: Comprehensive observability stack

---

## 📝 Conclusion

GenMentor represents a comprehensive AI-powered learning platform that combines:

- **Sophisticated AI Architecture**: 5 specialized modules với 15+ agents
- **Personalized Learning**: Adaptive profiling và content generation
- **Modern Tech Stack**: FastAPI, Streamlit, LangChain, ChromaDB
- **Flexible Configuration**: Multi-provider LLM support
- **Robust Engineering**: Error handling, parallel processing, state management

The system enables a complete personalized learning experience từ skill gap analysis đến interactive tutoring, với AI-driven content generation và adaptive profiling throughout the learning journey.

---

*Tài liệu này cung cấp cái nhìn toàn diện về GenMentor project architecture, implementation details, và operational workflows. Để biết thêm chi tiết kỹ thuật, tham khảo source code và configuration files.*
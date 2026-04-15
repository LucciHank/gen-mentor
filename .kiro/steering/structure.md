# Project Structure

## Repository Layout

```
gen-mentor/
├── backend/          # FastAPI backend service
├── frontend/         # Streamlit UI application
└── .kiro/           # Kiro AI assistant configuration
```

## Backend Structure

```
backend/
├── main.py                    # FastAPI app entry point, route definitions
├── api_schemas.py            # Pydantic request/response models
├── requirements.txt          # Python dependencies
│
├── config/                   # Hydra configuration
│   ├── main.yaml            # Main app config
│   ├── default.yaml         # Default module settings
│   ├── loader.py            # Config loading utilities
│   └── schemas.py           # Config validation schemas
│
├── base/                     # Core components and factories
│   ├── base_agent.py        # BaseAgent class for all agents
│   ├── llm_factory.py       # LLM provider factory
│   ├── rag_factory.py       # RAG system factory
│   ├── embedder_factory.py  # Embedding model factory
│   ├── searcher_factory.py  # Search provider factory
│   └── search_rag.py        # Search + RAG integration
│
├── modules/                  # Feature modules (agent-based)
│   ├── ai_chatbot_tutor/
│   ├── skill_gap_identification/
│   ├── adaptive_learner_modeling/
│   ├── personalized_resource_delivery/
│   └── learner_simulation/
│
├── utils/                    # Shared utilities
│   ├── config.py            # Config helpers
│   ├── llm_output.py        # LLM response processing
│   └── preprocess.py        # Document preprocessing
│
└── data/                     # Runtime data
    └── vectorstore/         # ChromaDB storage
```

## Frontend Structure

```
frontend/
├── main.py                   # Streamlit entry point, navigation
├── config.py                 # Frontend config (backend URL, mock mode)
├── requirements.txt          # Python dependencies
├── data_store.json          # Persistent UI state
│
├── .streamlit/
│   └── config.toml          # Streamlit theme/layout
│
├── assets/
│   ├── css/                 # UI styles
│   └── data_example/        # Mock data for offline mode
│
├── components/              # Reusable UI components
│   ├── chatbot/            # Chat interface
│   └── time_tracking/      # Session timing
│
├── pages/                   # Multi-page app screens
│   ├── onboarding.py       # Learner info collection
│   ├── goal_management.py  # Goal refinement
│   ├── learning_path.py    # Path scheduling/navigation
│   ├── knowledge_document.py  # In-session reading
│   └── dashboard.py        # Analytics overview
│
└── utils/                   # Frontend utilities
    ├── request_api.py      # Backend API client
    ├── state.py            # State management
    ├── formatting.py       # Display helpers
    └── colors.py           # Theme colors
```

## Module Architecture Pattern

Each backend module follows a consistent structure:

```
modules/{module_name}/
├── __init__.py              # Public API exports
├── schemas.py               # Pydantic data models
├── agents/                  # Agent implementations
│   ├── {agent_name}.py     # Agent class (extends BaseAgent)
│   └── __init__.py
└── prompts/                 # Prompt templates
    ├── {agent_name}.py     # Prompt strings/templates
    └── __init__.py
```

### Agent Pattern

All agents inherit from `BaseAgent` and follow this pattern:

1. **Initialization**: Takes an LLM instance and optional tools
2. **Prompt Management**: System prompts and task prompts
3. **Invocation**: `invoke(input_dict, task_prompt)` method
4. **Output Processing**: JSON output with optional "think" exclusion

### Module Examples

- **ai_chatbot_tutor**: Conversational tutoring agent
- **skill_gap_identification**: 
  - `SkillRequirementMapper`: Maps goals to required skills
  - `SkillGapIdentifier`: Identifies gaps from learner info
  - `LearningGoalRefiner`: Refines vague goals
- **adaptive_learner_modeling**:
  - `AdaptiveLearningProfiler`: Creates/updates learner profiles
- **personalized_resource_delivery**:
  - `LearningPathScheduler`: Generates learning sequences
  - `GoalOrientedKnowledgeExplorer`: Explores knowledge points
  - `SearchEnhancedKnowledgeDrafter`: Drafts content with RAG
  - `LearningDocumentIntegrator`: Combines drafts into documents
  - `DocumentQuizGenerator`: Creates assessments

## Configuration Management

- **Hydra-based**: YAML configs with composition and overrides
- **Environment variables**: API keys via `.env` files
- **Config hierarchy**: `default.yaml` → `main.yaml` → CLI overrides
- **Provider selection**: LLM, embedding, search providers configurable

## API Endpoint Patterns

FastAPI routes in `main.py` follow this pattern:

```python
@app.post("/endpoint-name")
async def endpoint_name(request: RequestSchema):
    llm = get_llm(request.model_provider, request.model_name)
    # Process request with appropriate agent/module
    result = module_function_with_llm(llm, ...)
    return {"result": result}
```

## Data Flow

1. **Frontend** → HTTP request → **Backend API**
2. **Backend** → Load config → Get LLM from factory
3. **Backend** → Instantiate agent → Invoke with prompt
4. **Agent** → Call LLM → Process response
5. **Backend** → Return JSON → **Frontend** renders

## State Management

- **Backend**: Stateless (each request independent)
- **Frontend**: 
  - Session state in `st.session_state`
  - Persistence via `data_store.json`
  - State utilities in `utils/state.py`

## Adding New Features

### Backend Module

1. Create `modules/new_feature/` directory
2. Add `schemas.py` with Pydantic models
3. Create `agents/{agent_name}.py` extending `BaseAgent`
4. Add `prompts/{agent_name}.py` with prompt templates
5. Export in `__init__.py`
6. Register endpoint in `main.py`
7. Add request schema to `api_schemas.py`

### Frontend Page

1. Create `pages/new_page.py`
2. Add API call in `utils/request_api.py`
3. Update navigation in `main.py`
4. Add mock data in `assets/data_example/` (optional)

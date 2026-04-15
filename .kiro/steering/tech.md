# Technology Stack

## Backend

### Core Framework
- **FastAPI**: Web framework for REST API endpoints
- **Python 3.12+**: Primary language
- **uvicorn**: ASGI server

### AI/ML Stack
- **LangChain**: LLM orchestration and agent framework
- **LangChain Community**: Extended integrations
- **LangGraph**: Agent workflow management

### LLM Providers (Configurable)
- DeepSeek (default: `deepseek-chat`, `deepseek-coder`)
- OpenAI (`gpt-4o`, `gpt-4o-mini`, `gpt-3.5-turbo`)
- Anthropic (`claude-3-5-sonnet`, `claude-3-sonnet`, `claude-3-haiku`)
- Google GenAI (`gemini-3-flash-preview`)
- Ollama (local models: `llama2`, `mistral`, `codellama`)

### Data & Search
- **ChromaDB**: Vector database for RAG
- **Sentence Transformers**: Text embeddings (`all-mpnet-base-v2`)
- **DuckDuckGo Search**: Web search integration
- **LangChain Docling**: Document processing

### Configuration
- **Hydra**: Configuration management with YAML
- **python-dotenv**: Environment variable management
- **Pydantic**: Data validation and API schemas

### Document Processing
- **pypdf**: PDF text extraction
- **pdfplumber**: Advanced PDF parsing
- **BeautifulSoup4**: HTML parsing

## Frontend

### Core Framework
- **Streamlit 1.40.0**: Web UI framework
- **Python**: UI logic

### Streamlit Extensions
- streamlit-card, streamlit-chat, streamlit-extras
- streamlit-tags, st-pages, streamlit-float
- streamlit-option-menu, streamlit-on-Hover-tabs
- extra-streamlit-components

### HTTP Client
- **httpx**: Async HTTP requests to backend

### Document Processing
- **pdfplumber**: PDF handling in UI
- **markdown**: Markdown rendering

## Common Commands

### Backend

```bash
# Setup
cd backend
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Run development server
uvicorn main:app --reload --host 0.0.0.0 --port 5000

# Run with specific config
python main.py --config-name=prod

# Testing
python -m pytest test_config.py
```

### Frontend

```bash
# Setup
cd frontend
uv venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv pip install -r requirements.txt

# Run UI (live backend)
streamlit run main.py

# Run UI (mock mode - no backend needed)
# Edit config.py: set use_mock_data = True
streamlit run main.py
```

### Environment Variables

Required API keys (set in `.env` or environment):
```bash
DEEPSEEK_API_KEY=your-key
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
OLLAMA_BASE_URL=http://localhost:11434
```

## Package Management

- **uv**: Fast Python package installer (preferred)
- Alternative: pip with requirements.txt

## Configuration Files

- `backend/config/main.yaml`: Main application config
- `backend/config/default.yaml`: Default module settings
- `frontend/config.py`: Frontend configuration
- `frontend/.streamlit/config.toml`: Streamlit theme/layout

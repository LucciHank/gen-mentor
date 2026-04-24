# GenMentor - AI-Powered Personalized Learning Platform

GenMentor is an intelligent learning platform that creates adaptive, personalized learning experiences tailored to individual learners' needs, skill gaps, and career goals.

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- PostgreSQL 12+
- Git

### One-Command Setup
```bash
python setup_mvp.py
```

This will:
- Set up backend and frontend virtual environments
- Install all dependencies
- Create database schema and seed data
- Generate startup scripts

### Manual Setup
```bash
# 1. Clone and setup backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with your configuration

# 2. Setup database
python scripts/setup_database.py
python scripts/ingest_documents.py

# 3. Setup frontend
cd ../frontend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 4. Start services
# Terminal 1 - Backend
cd backend && python main.py

# Terminal 2 - Frontend  
cd frontend && streamlit run main.py
```

## 🏗️ Architecture

### Backend (FastAPI)
- **Core Framework**: FastAPI with Python 3.12+
- **AI/ML Stack**: LangChain, LangGraph for agent orchestration
- **LLM Providers**: DeepSeek, OpenAI, Anthropic, Google GenAI, Ollama
- **Data Storage**: PostgreSQL + ChromaDB vector store
- **Document Processing**: PDF, DOCX, Excel parsing and indexing

### Frontend (Streamlit)
- **UI Framework**: Streamlit with custom components
- **Features**: Multi-page app with file upload, chat interface, progress tracking
- **Integration**: RESTful API client for backend communication

### Key Components
```
├── backend/                 # FastAPI backend service
│   ├── modules/            # AI agent modules
│   ├── base/               # Core factories and utilities  
│   ├── config/             # Hydra configuration
│   ├── scripts/            # Setup and ingestion scripts
│   └── main.py             # API server entry point
├── frontend/               # Streamlit UI application
│   ├── pages/              # Multi-page interface
│   ├── components/         # Reusable UI components
│   └── utils/              # Frontend utilities
└── seed_data/              # Sample data and schemas
    ├── raw/                # Sample documents
    ├── taxonomy/           # Skills and roles definitions
    └── database/           # Database schema
```

## 🎯 Core Features

### 🔍 Skill Gap Analysis
- Upload CV/resume for automatic skill extraction
- Compare current skills against target role requirements
- Identify specific knowledge gaps and learning priorities

### 🎓 Adaptive Learning Paths
- Generate personalized learning sequences
- Adjust content based on learner progress and feedback
- Support multiple learning styles and time commitments

### 🤖 AI Tutoring
- Interactive conversational learning with context-aware responses
- Real-time Q&A support during learning sessions
- Personalized explanations based on learner profile

### 📚 Content Generation
- Create tailored learning materials from knowledge base
- Generate assessments and quizzes automatically
- Integrate multiple knowledge sources with RAG

### 📊 Progress Tracking
- Monitor learning progress across sessions
- Adaptive scheduling based on performance
- Detailed analytics and recommendations

## 🛠️ API Endpoints

### Document Management
- `POST /documents/upload` - Upload learning materials
- `GET /documents` - List available documents
- `POST /knowledge/search` - Search knowledge base

### Learner Intake
- `POST /cv/parse` - Parse CV and extract skills
- `POST /diagnostic/generate` - Generate skill assessment
- `POST /learner-profile/build` - Build comprehensive learner profile

### Learning Path
- `POST /learning-path/generate` - Create personalized learning path
- `POST /learning-path/reschedule` - Adjust path based on progress

### Learning Runtime
- `POST /lesson/generate` - Generate lesson content
- `POST /quiz/generate` - Create assessments
- `POST /tutor/chat` - Interactive AI tutoring

## 📋 Configuration

### Environment Variables
```bash
# Database
DB_HOST=localhost
DB_NAME=genmentor
DB_USER=postgres
DB_PASSWORD=your_password

# LLM API Keys
DEEPSEEK_API_KEY=your_key
OPENAI_API_KEY=your_key
ANTHROPIC_API_KEY=your_key

# Application
LOG_LEVEL=debug
SERVER_PORT=5000
```

### LLM Providers
Configure in `backend/config/main.yaml`:
```yaml
llm:
  provider: "deepseek"  # deepseek, openai, anthropic, google, ollama
  model_name: "deepseek-chat"
  
embedder:
  provider: "sentence-transformers"
  model_name: "all-mpnet-base-v2"
```

## 🧪 Testing

### API Testing
```bash
# Test API endpoints
curl http://localhost:5000/docs  # Swagger documentation
curl http://localhost:5000/list-llm-models

# Upload document
curl -X POST "http://localhost:5000/documents/upload" \
  -F "file=@sample.pdf" \
  -F "category=AI" \
  -F "title=Sample Document"
```

### Frontend Testing
1. Navigate to http://localhost:8501
2. Test file upload functionality
3. Try CV parsing and skill analysis
4. Generate a learning path
5. Chat with AI tutor

## 📊 Sample Data

The project includes comprehensive seed data:

### Documents (21 files)
- **AI/ML**: Fundamentals, algorithms, frameworks
- **ERP/SOP**: Implementation guides, configuration manuals
- **Software Process**: API design, testing, project management
- **Assessments**: Question banks and rubrics

### Taxonomy
- **5 Roles**: AI Engineer, Data Scientist, Software Developer, ERP Consultant, Business Analyst
- **10 Skills**: Python, ML, Deep Learning, SQL, API Development, etc.
- **Role-Skill Mappings**: Requirements and proficiency levels

## 🔄 Development Workflow

### Adding New Features

1. **Backend Module**:
   ```bash
   # Create new module
   mkdir backend/modules/new_feature
   # Add agent, prompts, schemas
   # Register in main.py
   ```

2. **Frontend Page**:
   ```bash
   # Create new page
   touch frontend/pages/new_page.py
   # Add to navigation in main.py
   ```

3. **Database Changes**:
   ```bash
   # Update schema
   vim seed_data/database/minimal_schema.sql
   # Run migration
   python backend/scripts/setup_database.py
   ```

### Code Style
- Follow PEP 8 for Python code
- Use type hints for function signatures
- Document modules and complex functions
- Use meaningful variable and function names

## 🚀 Deployment

### Production Setup
1. Use environment-specific configuration
2. Set up proper database with connection pooling
3. Configure reverse proxy (nginx)
4. Set up SSL certificates
5. Use production WSGI server (gunicorn)
6. Set up monitoring and logging

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

### Common Issues
- **Database connection**: Check PostgreSQL is running and credentials are correct
- **API errors**: Check logs in `backend/backend-live-err.log`
- **Frontend issues**: Check Streamlit logs and browser console

### Getting Help
- Check the [Phase A Checklist](PHASE_A_CHECKLIST.md) for setup guidance
- Review configuration in `.kiro/steering/` directory
- Open an issue for bugs or feature requests

## 🎯 Roadmap

### Phase A ✅ (Current)
- Core infrastructure and basic APIs
- Database setup and seed data
- MVP functionality

### Phase B 🔄 (Next)
- Advanced NLP for CV parsing
- Sophisticated diagnostic algorithms
- Real-time progress tracking
- Enhanced UI/UX

### Phase C 📋 (Future)
- Multi-language support
- Mobile app
- Advanced analytics
- Enterprise features

---

**Built with ❤️ using FastAPI, Streamlit, and LangChain**
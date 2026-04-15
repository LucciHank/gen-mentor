# GenMentor Product Overview

GenMentor is an AI-powered personalized learning platform that creates adaptive learning experiences tailored to individual learners' needs, skill gaps, and goals.

## Core Capabilities

- **Skill Gap Analysis**: Analyzes learner profiles (including CV uploads) to identify knowledge gaps between current skills and learning objectives
- **Adaptive Learning Paths**: Generates personalized learning sequences with structured session planning
- **AI Tutoring**: Interactive conversational learning with context-aware responses
- **Content Generation**: Creates tailored learning materials, knowledge documents, and assessments
- **Learner Modeling**: Maintains and updates detailed learner profiles that adapt based on interactions

## Key Features

- Learning goal refinement and clarification
- Skill requirement mapping for specific goals
- Multi-perspective knowledge point exploration
- Document integration from various knowledge sources
- Automated quiz generation (single-choice, multiple-choice, true/false, short answer)
- Search-enhanced content drafting with RAG (Retrieval-Augmented Generation)

## Architecture

The system uses a modular architecture with specialized agents for different educational tasks, backed by LLM orchestration through LangChain and configurable via Hydra. The platform supports multiple LLM providers (DeepSeek, OpenAI, Anthropic, Ollama) and integrates web search and vector storage for enhanced content generation.

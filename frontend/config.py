backend_endpoint = "http://127.0.0.1:5000/"
use_mock_data = True
use_search = True

# MVP API endpoints
MVP_ENDPOINTS = {
    "upload_document": "documents/upload",
    "list_documents": "documents",
    "search_knowledge": "knowledge/search",
    "get_document": "documents/{document_id}",
    "parse_cv": "cv/parse",
    "generate_diagnostic": "diagnostic/generate",
    "submit_diagnostic": "diagnostic/submit",
    "build_learner_profile": "learner-profile/build",
    "generate_learning_path": "learning-path/generate",
    "reschedule_learning_path": "learning-path/reschedule",
    "generate_lesson": "lesson/generate",
    "generate_quiz": "quiz/generate",
    "chat_tutor": "tutor/chat",
    "update_progress": "learner-progress/update",
    "get_role_requirements": "roles/{role_id}/requirements",
    "list_roles": "roles",
    "list_skills": "skills",
}

UI_CONFIG = {
    "app_title": "GenMentor - AI-Powered Learning Platform",
    "sidebar_title": "Navigation",
    "max_file_size": 10 * 1024 * 1024,
    "supported_file_types": ["pdf", "docx", "txt"],
    "default_session_count": 12,
    "default_time_commitment": "2 hours/week",
}

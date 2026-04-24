#!/usr/bin/env python3
"""
GenMentor MVP - Simple Demo Version
Simplified backend without database dependencies
"""

import json
import logging
from typing import Dict, Any, List, Optional
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="GenMentor API - Demo",
    description="AI-powered personalized learning platform - Demo Version",
    version="1.0.0-demo"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for demo
demo_data = {
    "learners": {},
    "learning_paths": {},
    "documents": []
}

# Pydantic models
class CVParseRequest(BaseModel):
    cv_text: Optional[str] = None

class CVParseResponse(BaseModel):
    extracted_info: Dict[str, Any]
    skills_identified: List[str]
    experience_summary: str

class DiagnosticGenerateRequest(BaseModel):
    learner_profile: Dict[str, Any]
    target_role: str
    skill_gaps: List[str]
    question_count: int = 10

class LearnerProfileBuildRequest(BaseModel):
    learner_info: Dict[str, Any]
    cv_analysis: Dict[str, Any]
    diagnostic_results: Dict[str, Any]
    learning_goals: List[str]

class LearningPathGenerateRequest(BaseModel):
    learner_profile: Dict[str, Any]
    target_role: str
    time_commitment: str
    duration_weeks: int = 12

# API Routes
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "GenMentor API Demo",
        "version": "1.0.0-demo",
        "status": "running",
        "endpoints": [
            "/docs",
            "/cv/parse",
            "/diagnostic/generate",
            "/learner-profile/build",
            "/learning-path/generate",
            "/documents/upload"
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "GenMentor API is running"}

@app.post("/cv/parse", response_model=CVParseResponse)
async def parse_cv(request: CVParseRequest):
    """Parse CV and extract structured information"""
    try:
        # Mock CV parsing for demo
        extracted_info = {
            "name": "Nguyễn Văn An",
            "email": "nguyen.van.an@email.com",
            "phone": "+84 123 456 789",
            "experience_years": 3,
            "education": ["Cử nhân Khoa học Máy tính - ĐH Bách Khoa"],
            "certifications": ["AWS Cloud Practitioner"],
            "current_position": "Software Developer"
        }
        
        skills_identified = [
            "Python", "JavaScript", "SQL", "Git", 
            "React", "Node.js", "MongoDB", "Docker"
        ]
        
        experience_summary = "3 năm kinh nghiệm phát triển phần mềm với chuyên môn về Python và JavaScript. Có kinh nghiệm làm việc với các framework hiện đại và công nghệ cloud."
        
        return CVParseResponse(
            extracted_info=extracted_info,
            skills_identified=skills_identified,
            experience_summary=experience_summary
        )
        
    except Exception as e:
        logger.error(f"Error parsing CV: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/diagnostic/generate")
async def generate_diagnostic(request: DiagnosticGenerateRequest):
    """Generate diagnostic assessment"""
    try:
        # Mock diagnostic generation
        questions = []
        skills = ["Python", "Machine Learning", "Data Analysis", "Deep Learning", "SQL"]
        
        for i, skill in enumerate(skills[:request.question_count]):
            questions.append({
                "id": i + 1,
                "skill": skill,
                "question": f"Đánh giá mức độ hiểu biết của bạn về {skill}?",
                "type": "multiple_choice",
                "options": ["Mới bắt đầu", "Cơ bản", "Trung bình", "Nâng cao", "Chuyên gia"],
                "weight": 1.0
            })
        
        diagnostic_id = f"diag_{len(demo_data['learners']) + 1}"
        
        return {
            "diagnostic_id": diagnostic_id,
            "questions": questions,
            "estimated_time": len(questions) * 2,
            "instructions": "Hãy trả lời thành thật để chúng tôi có thể tạo lộ trình phù hợp nhất"
        }
        
    except Exception as e:
        logger.error(f"Error generating diagnostic: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/diagnostic/submit")
async def submit_diagnostic(diagnostic_id: str, answers: Dict[str, str]):
    """Submit diagnostic assessment results"""
    try:
        # Process answers and calculate skill levels
        skill_levels = {}
        for question_id, answer in answers.items():
            level_map = {
                "Mới bắt đầu": 1,
                "Cơ bản": 2, 
                "Trung bình": 3,
                "Nâng cao": 4,
                "Chuyên gia": 5
            }
            skill_levels[f"skill_{question_id}"] = level_map.get(answer, 1)
        
        results = {
            "diagnostic_id": diagnostic_id,
            "skill_levels": skill_levels,
            "overall_score": sum(skill_levels.values()) / len(skill_levels),
            "completion_date": "2024-04-22T10:00:00Z",
            "recommendations": [
                "Tập trung vào Machine Learning cơ bản",
                "Nâng cao kỹ năng Python programming",
                "Học thêm về Data Analysis"
            ]
        }
        
        return {"results": results, "status": "completed"}
        
    except Exception as e:
        logger.error(f"Error submitting diagnostic: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learner-profile/build")
async def build_learner_profile(request: LearnerProfileBuildRequest):
    """Build comprehensive learner profile"""
    try:
        # Mock learner profile building
        learner_profile = {
            "id": f"learner_{len(demo_data['learners']) + 1}",
            "personal_info": request.learner_info,
            "current_skills": {
                "Python": "intermediate",
                "JavaScript": "intermediate", 
                "SQL": "beginner",
                "Machine Learning": "beginner"
            },
            "skill_gaps": [
                {
                    "skill": "Deep Learning",
                    "current_level": "beginner",
                    "target_level": "intermediate",
                    "priority": "high"
                },
                {
                    "skill": "Data Science",
                    "current_level": "beginner", 
                    "target_level": "advanced",
                    "priority": "high"
                }
            ],
            "learning_preferences": {
                "style": ["video", "hands-on"],
                "pace": "moderate",
                "time_availability": "6 hours/week"
            },
            "goals": request.learning_goals,
            "created_at": "2024-04-22T10:00:00Z"
        }
        
        # Store in demo data
        demo_data["learners"][learner_profile["id"]] = learner_profile
        
        return {"learner_profile": learner_profile}
        
    except Exception as e:
        logger.error(f"Error building learner profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/learning-path/generate")
async def generate_learning_path(request: LearningPathGenerateRequest):
    """Generate personalized learning path"""
    try:
        # Mock learning path generation
        sessions = []
        
        # Generate sample sessions
        topics = [
            "Python Fundamentals",
            "Data Structures & Algorithms", 
            "Introduction to Machine Learning",
            "Data Analysis with Pandas",
            "Data Visualization",
            "Statistical Analysis",
            "Machine Learning Algorithms",
            "Deep Learning Basics",
            "Neural Networks",
            "Model Evaluation",
            "MLOps Fundamentals",
            "Capstone Project"
        ]
        
        for i, topic in enumerate(topics):
            sessions.append({
                "session_number": i + 1,
                "title": topic,
                "description": f"Học về {topic} với các bài tập thực hành",
                "duration_minutes": 120,
                "type": "mixed",
                "activities": ["video", "reading", "practice", "quiz"],
                "prerequisites": sessions[i-1]["title"] if i > 0 else None,
                "learning_objectives": [
                    f"Hiểu khái niệm cơ bản về {topic}",
                    f"Áp dụng {topic} vào bài tập thực tế",
                    f"Đánh giá và cải thiện kỹ năng {topic}"
                ]
            })
        
        learning_path = {
            "id": f"path_{len(demo_data['learning_paths']) + 1}",
            "learner_id": request.learner_profile.get("id", "demo_learner"),
            "title": f"Lộ trình {request.target_role}",
            "description": f"Lộ trình cá nhân hóa để trở thành {request.target_role}",
            "target_role": request.target_role,
            "duration_weeks": request.duration_weeks,
            "total_hours": len(sessions) * 2,
            "sessions": sessions,
            "milestones": [
                {
                    "week": 4,
                    "title": "Python Mastery",
                    "description": "Hoàn thành các kỹ năng Python cơ bản"
                },
                {
                    "week": 8, 
                    "title": "Data Analysis Skills",
                    "description": "Thành thạo phân tích dữ liệu"
                },
                {
                    "week": 12,
                    "title": "ML Project Ready", 
                    "description": "Sẵn sàng cho dự án Machine Learning"
                }
            ],
            "created_at": "2024-04-22T10:00:00Z"
        }
        
        # Store in demo data
        demo_data["learning_paths"][learning_path["id"]] = learning_path
        
        return learning_path
        
    except Exception as e:
        logger.error(f"Error generating learning path: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(...),
    title: Optional[str] = Form(None)
):
    """Upload and process a document"""
    try:
        # Mock document upload
        doc_id = len(demo_data["documents"]) + 1
        
        document = {
            "id": doc_id,
            "filename": file.filename,
            "title": title or file.filename,
            "category": category,
            "file_type": file.filename.split('.')[-1].lower(),
            "size": file.size if hasattr(file, 'size') else 0,
            "uploaded_at": "2024-04-22T10:00:00Z",
            "status": "processed"
        }
        
        demo_data["documents"].append(document)
        
        return {
            "document_id": doc_id,
            "filename": file.filename,
            "status": "success",
            "message": "Document uploaded and processed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/documents")
async def list_documents(category: Optional[str] = None):
    """List all documents with optional filtering"""
    try:
        documents = demo_data["documents"]
        
        if category:
            documents = [doc for doc in documents if doc["category"] == category]
        
        return {"documents": documents, "total": len(documents)}
        
    except Exception as e:
        logger.error(f"Error listing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/demo-data")
async def get_demo_data():
    """Get all demo data for debugging"""
    return demo_data

@app.delete("/demo-data")
async def clear_demo_data():
    """Clear all demo data"""
    demo_data["learners"].clear()
    demo_data["learning_paths"].clear()
    demo_data["documents"].clear()
    return {"message": "Demo data cleared"}

if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app", 
        host="0.0.0.0", 
        port=5000, 
        log_level="info",
        reload=True
    )
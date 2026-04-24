#!/usr/bin/env python3
"""
GenMentor Frontend - Simple Demo Version
Streamlit app for testing backend APIs
"""

import streamlit as st
import httpx
import json
from typing import Dict, Any, List

# Configure page
st.set_page_config(
    page_title="GenMentor - AI Learning Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Backend URL
BACKEND_URL = "http://localhost:5000"

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #007AFF;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .section-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1D1D1F;
        margin: 2rem 0 1rem 0;
        border-bottom: 2px solid #007AFF;
        padding-bottom: 0.5rem;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .info-box {
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def call_api(endpoint: str, method: str = "GET", data: Dict = None) -> Dict:
    """Call backend API"""
    try:
        url = f"{BACKEND_URL}{endpoint}"
        
        with httpx.Client() as client:
            if method == "GET":
                response = client.get(url)
            elif method == "POST":
                response = client.post(url, json=data)
            else:
                return {"error": f"Unsupported method: {method}"}
        
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code} - {response.text}"}
    
    except Exception as e:
        return {"error": f"Connection Error: {str(e)}"}

def main():
    """Main app"""
    
    # Header
    st.markdown('<h1 class="main-header">🎓 GenMentor Demo</h1>', unsafe_allow_html=True)
    st.markdown("**AI-Powered Personalized Learning Platform**")
    
    # Sidebar
    with st.sidebar:
        st.title("🚀 Demo Features")
        
        demo_option = st.selectbox(
            "Choose Demo:",
            [
                "🏠 API Status",
                "📄 CV Parser", 
                "🧠 Diagnostic Generator",
                "👤 Learner Profile Builder",
                "🛤️ Learning Path Generator",
                "📚 Document Upload",
                "🔍 API Explorer"
            ]
        )
    
    # Main content based on selection
    if demo_option == "🏠 API Status":
        show_api_status()
    elif demo_option == "📄 CV Parser":
        show_cv_parser()
    elif demo_option == "🧠 Diagnostic Generator":
        show_diagnostic_generator()
    elif demo_option == "👤 Learner Profile Builder":
        show_profile_builder()
    elif demo_option == "🛤️ Learning Path Generator":
        show_path_generator()
    elif demo_option == "📚 Document Upload":
        show_document_upload()
    elif demo_option == "🔍 API Explorer":
        show_api_explorer()

def show_api_status():
    """Show API status"""
    st.markdown('<h2 class="section-header">API Status Check</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Check Backend Status", type="primary"):
            with st.spinner("Checking backend..."):
                result = call_api("/")
                
                if "error" in result:
                    st.markdown(f'<div class="error-box">❌ Backend Error: {result["error"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="success-box">✅ Backend is running!</div>', unsafe_allow_html=True)
                    st.json(result)
    
    with col2:
        if st.button("💚 Health Check", type="secondary"):
            with st.spinner("Checking health..."):
                result = call_api("/health")
                
                if "error" in result:
                    st.markdown(f'<div class="error-box">❌ Health Check Failed: {result["error"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="success-box">✅ System Healthy!</div>', unsafe_allow_html=True)
                    st.json(result)

def show_cv_parser():
    """Show CV parser demo"""
    st.markdown('<h2 class="section-header">CV Parser Demo</h2>', unsafe_allow_html=True)
    
    st.markdown("### 📝 Test CV Parsing")
    st.info("This demo uses mock data to simulate CV parsing functionality.")
    
    cv_text = st.text_area(
        "Enter CV text (optional - will use mock data):",
        placeholder="Paste your CV content here...",
        height=150
    )
    
    if st.button("🔍 Parse CV", type="primary"):
        with st.spinner("Parsing CV..."):
            data = {"cv_text": cv_text} if cv_text else {}
            result = call_api("/cv/parse", "POST", data)
            
            if "error" in result:
                st.markdown(f'<div class="error-box">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">✅ CV Parsed Successfully!</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("👤 Extracted Information")
                    st.json(result["extracted_info"])
                
                with col2:
                    st.subheader("🛠️ Skills Identified")
                    for skill in result["skills_identified"]:
                        st.badge(skill)
                
                st.subheader("📋 Experience Summary")
                st.write(result["experience_summary"])

def show_diagnostic_generator():
    """Show diagnostic generator demo"""
    st.markdown('<h2 class="section-header">Diagnostic Generator Demo</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🧠 Generate Skill Assessment")
    
    col1, col2 = st.columns(2)
    
    with col1:
        target_role = st.selectbox(
            "Target Role:",
            ["AI Engineer", "Data Scientist", "Software Developer", "ML Engineer"]
        )
        
        question_count = st.slider("Number of Questions:", 5, 15, 10)
    
    with col2:
        skill_gaps = st.multiselect(
            "Skill Gaps to Assess:",
            ["Python", "Machine Learning", "Deep Learning", "Data Analysis", "SQL", "Statistics"],
            default=["Python", "Machine Learning"]
        )
    
    if st.button("🎯 Generate Diagnostic", type="primary"):
        with st.spinner("Generating diagnostic..."):
            data = {
                "learner_profile": {"name": "Demo User"},
                "target_role": target_role,
                "skill_gaps": skill_gaps,
                "question_count": question_count
            }
            
            result = call_api("/diagnostic/generate", "POST", data)
            
            if "error" in result:
                st.markdown(f'<div class="error-box">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="success-box">✅ Diagnostic Generated!</div>', unsafe_allow_html=True)
                
                st.subheader(f"📝 Assessment: {result['diagnostic_id']}")
                st.info(f"⏱️ Estimated time: {result['estimated_time']} minutes")
                
                for i, question in enumerate(result["questions"], 1):
                    with st.expander(f"Question {i}: {question['skill']}"):
                        st.write(f"**{question['question']}**")
                        
                        # Create interactive question
                        answer = st.radio(
                            "Your answer:",
                            question["options"],
                            key=f"q_{i}",
                            horizontal=True
                        )
                        
                        if st.button(f"Submit Answer {i}", key=f"submit_{i}"):
                            st.success(f"Answer recorded: {answer}")

def show_profile_builder():
    """Show learner profile builder demo"""
    st.markdown('<h2 class="section-header">Learner Profile Builder Demo</h2>', unsafe_allow_html=True)
    
    st.markdown("### 👤 Build Comprehensive Learner Profile")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Personal Information")
            name = st.text_input("Name", value="Demo User")
            email = st.text_input("Email", value="demo@example.com")
            experience = st.selectbox("Experience Level", ["Beginner", "Intermediate", "Advanced"])
        
        with col2:
            st.subheader("Learning Goals")
            goals = st.multiselect(
                "Select Learning Goals:",
                ["Become AI Engineer", "Learn Machine Learning", "Master Python", "Data Science Skills"],
                default=["Become AI Engineer"]
            )
        
        st.subheader("CV Analysis Results")
        cv_analysis = st.text_area(
            "CV Analysis (mock data):",
            value='{"skills": ["Python", "JavaScript"], "experience_years": 3}',
            height=100
        )
        
        st.subheader("Diagnostic Results")
        diagnostic_results = st.text_area(
            "Diagnostic Results (mock data):",
            value='{"overall_score": 3.2, "skill_levels": {"Python": 3, "ML": 2}}',
            height=100
        )
        
        submitted = st.form_submit_button("🚀 Build Profile", type="primary")
        
        if submitted:
            with st.spinner("Building learner profile..."):
                data = {
                    "learner_info": {"name": name, "email": email, "experience": experience},
                    "cv_analysis": json.loads(cv_analysis) if cv_analysis else {},
                    "diagnostic_results": json.loads(diagnostic_results) if diagnostic_results else {},
                    "learning_goals": goals
                }
                
                result = call_api("/learner-profile/build", "POST", data)
                
                if "error" in result:
                    st.markdown(f'<div class="error-box">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-box">✅ Learner Profile Created!</div>', unsafe_allow_html=True)
                    
                    profile = result["learner_profile"]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("👤 Profile Overview")
                        st.write(f"**ID:** {profile['id']}")
                        st.write(f"**Created:** {profile['created_at']}")
                        
                        st.subheader("🎯 Learning Goals")
                        for goal in profile['goals']:
                            st.write(f"• {goal}")
                    
                    with col2:
                        st.subheader("🛠️ Current Skills")
                        for skill, level in profile['current_skills'].items():
                            st.write(f"**{skill}:** {level}")
                        
                        st.subheader("📈 Skill Gaps")
                        for gap in profile['skill_gaps']:
                            st.write(f"• **{gap['skill']}:** {gap['current_level']} → {gap['target_level']}")

def show_path_generator():
    """Show learning path generator demo"""
    st.markdown('<h2 class="section-header">Learning Path Generator Demo</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🛤️ Generate Personalized Learning Path")
    
    with st.form("path_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            target_role = st.selectbox(
                "Target Role:",
                ["AI Engineer", "Data Scientist", "Software Developer", "ML Engineer"]
            )
            
            duration_weeks = st.slider("Duration (weeks):", 4, 24, 12)
        
        with col2:
            time_commitment = st.selectbox(
                "Time Commitment:",
                ["2 hours/week", "4 hours/week", "6 hours/week", "8 hours/week", "10+ hours/week"]
            )
        
        learner_profile = st.text_area(
            "Learner Profile (JSON):",
            value='{"id": "demo_learner", "current_skills": {"Python": "intermediate"}, "goals": ["AI Engineer"]}',
            height=100
        )
        
        submitted = st.form_submit_button("🎯 Generate Learning Path", type="primary")
        
        if submitted:
            with st.spinner("Generating learning path..."):
                data = {
                    "learner_profile": json.loads(learner_profile),
                    "target_role": target_role,
                    "time_commitment": time_commitment,
                    "duration_weeks": duration_weeks
                }
                
                result = call_api("/learning-path/generate", "POST", data)
                
                if "error" in result:
                    st.markdown(f'<div class="error-box">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-box">✅ Learning Path Generated!</div>', unsafe_allow_html=True)
                    
                    # Path overview
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("📅 Duration", f"{result['duration_weeks']} weeks")
                    with col2:
                        st.metric("⏱️ Total Hours", f"{result['total_hours']}h")
                    with col3:
                        st.metric("📚 Sessions", len(result['sessions']))
                    
                    # Milestones
                    st.subheader("🎯 Milestones")
                    for milestone in result['milestones']:
                        st.info(f"**Week {milestone['week']}:** {milestone['title']} - {milestone['description']}")
                    
                    # Sessions
                    st.subheader("📚 Learning Sessions")
                    for session in result['sessions'][:5]:  # Show first 5 sessions
                        with st.expander(f"Session {session['session_number']}: {session['title']}"):
                            st.write(f"**Description:** {session['description']}")
                            st.write(f"**Duration:** {session['duration_minutes']} minutes")
                            st.write(f"**Type:** {session['type']}")
                            st.write(f"**Activities:** {', '.join(session['activities'])}")
                            
                            if session['prerequisites']:
                                st.write(f"**Prerequisites:** {session['prerequisites']}")
                    
                    if len(result['sessions']) > 5:
                        st.info(f"... and {len(result['sessions']) - 5} more sessions")

def show_document_upload():
    """Show document upload demo"""
    st.markdown('<h2 class="section-header">Document Upload Demo</h2>', unsafe_allow_html=True)
    
    st.markdown("### 📚 Upload Learning Materials")
    
    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['pdf', 'docx', 'txt', 'md'],
        help="Upload learning materials to be processed"
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        category = st.selectbox(
            "Document Category:",
            ["AI", "Programming", "Data Science", "General", "Tutorial"]
        )
    
    with col2:
        title = st.text_input("Document Title (optional)")
    
    if uploaded_file and st.button("📤 Upload Document", type="primary"):
        with st.spinner("Uploading document..."):
            # Mock upload for demo
            result = {
                "document_id": 123,
                "filename": uploaded_file.name,
                "status": "success",
                "message": "Document uploaded and processed successfully"
            }
            
            st.markdown('<div class="success-box">✅ Document Uploaded Successfully!</div>', unsafe_allow_html=True)
            st.json(result)
    
    # List documents
    if st.button("📋 List Documents"):
        with st.spinner("Loading documents..."):
            result = call_api("/documents")
            
            if "error" in result:
                st.markdown(f'<div class="error-box">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
            else:
                st.subheader("📚 Document Library")
                if result["documents"]:
                    for doc in result["documents"]:
                        with st.expander(f"📄 {doc['title']}"):
                            st.write(f"**Category:** {doc['category']}")
                            st.write(f"**Type:** {doc['file_type']}")
                            st.write(f"**Uploaded:** {doc['uploaded_at']}")
                            st.write(f"**Status:** {doc['status']}")
                else:
                    st.info("No documents uploaded yet.")

def show_api_explorer():
    """Show API explorer"""
    st.markdown('<h2 class="section-header">API Explorer</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🔍 Test API Endpoints")
    
    col1, col2 = st.columns(2)
    
    with col1:
        endpoint = st.selectbox(
            "Select Endpoint:",
            [
                "/",
                "/health", 
                "/cv/parse",
                "/diagnostic/generate",
                "/learner-profile/build",
                "/learning-path/generate",
                "/documents",
                "/demo-data"
            ]
        )
        
        method = st.selectbox("Method:", ["GET", "POST"])
    
    with col2:
        if method == "POST":
            request_data = st.text_area(
                "Request Data (JSON):",
                value='{}',
                height=150
            )
        else:
            request_data = "{}"
    
    if st.button("🚀 Send Request", type="primary"):
        with st.spinner("Sending request..."):
            try:
                data = json.loads(request_data) if method == "POST" else None
                result = call_api(endpoint, method, data)
                
                if "error" in result:
                    st.markdown(f'<div class="error-box">❌ Error: {result["error"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown('<div class="success-box">✅ Request Successful!</div>', unsafe_allow_html=True)
                    st.json(result)
            
            except json.JSONDecodeError:
                st.error("Invalid JSON in request data")

if __name__ == "__main__":
    main()
"""Screen 5 — Lesson / Video Player"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.mock_data import LESSON_CONTENT
from components.ai_coach import render_ai_coach
from components.quick_review import render_quick_review
from components.topbar import render_topbar

st.set_page_config(page_title="GenMentor — Lesson", page_icon="🧠", layout="wide")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)


def render_lesson():
    render_topbar()

    lesson = LESSON_CONTENT
    st.markdown(f"<h1>{lesson['title']}</h1>", unsafe_allow_html=True)
    st.markdown(f'<div style="color:var(--text-secondary); margin-bottom: 2rem;">{lesson["module"]} · {lesson["duration"]} phút · {_type_label(lesson["type"])}</div>', unsafe_allow_html=True)

    col_content, col_coach = st.columns([1.8, 1], gap="large")

    with col_content:
        # Video placeholder
        if lesson["type"] == "video":
            st.markdown(
                """
                <div class="gm-card" style="background:#000; border-radius:24px; text-align:center; padding:100px 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.2);">
                    <div style="font-size:60px; filter: drop-shadow(0 0 20px rgba(255,255,255,0.4));">▶️</div>
                    <p style="color:#888; margin-top:20px; font-weight:500;">VIDEO LECTURE PLAYER</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Transcript / reading content
        st.markdown('<div class="gm-card">', unsafe_allow_html=True)
        st.markdown('<div class="gm-label-caps">📄 Nội dung bài học</div>', unsafe_allow_html=True)
        st.markdown(f"<div style='font-size:16px; line-height:1.6;'>{lesson['transcript']}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Inline notes
        st.markdown('<div class="gm-card">', unsafe_allow_html=True)
        st.markdown('<div class="gm-label-caps">📝 Ghi chú của bạn</div>', unsafe_allow_html=True)
        st.text_area("Viết ghi chú...", key="lesson_notes", height=120, label_visibility="collapsed")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_coach:
        render_ai_coach(lesson)

    # Footer — completion
    st.markdown('<div class="gm-card">', unsafe_allow_html=True)
    st.markdown('<div class="gm-label-caps">✅ Hoàn thành bài học?</div>', unsafe_allow_html=True)
    
    理解 = st.radio("Mức độ hiểu bài của bạn:", ["Chưa hiểu", "Tạm ổn", "Rất tốt"], horizontal=True, key="lesson_understanding")
    
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("Làm Quiz ngay", type="primary", use_container_width=True):
            render_quick_review()
    with c2:
        if st.button("Bài học tiếp theo", use_container_width=True):
            st.session_state["selected_screen"] = "module_detail"
            st.switch_page("pages/module_detail.py")
    with c3:
        if st.button("Dời sang ngày mai", use_container_width=True, kind="secondary"):
            st.info("Đã cập nhật lộ trình.")
    st.markdown('</div>', unsafe_allow_html=True)


def _type_label(t):
    return {"video": "Video", "reading": "Đọc", "quiz": "Quiz", "practice": "Thực hành"}.get(t, t)


render_lesson()

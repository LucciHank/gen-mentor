"""Screen 4 — Chi tiết chặng / Module"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.mock_data import CURRENT_MODULE
from components.topbar import render_topbar

st.set_page_config(page_title="GenMentor — Module", page_icon="🧠", layout="wide")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)


def _lesson_icon(t):
    return {"video": "🎬", "quiz": "📝", "reading": "📖", "practice": "💻"}.get(t, "📌")


def _lesson_status(status):
    cls = {"completed": "gm-badge-completed", "in_progress": "gm-badge-in-progress", "not_started": "gm-badge-not-started", "needs_review": "gm-badge-overdue"}.get(status, "gm-badge-not-started")
    label = {"completed": "Xong", "in_progress": "Đang học", "not_started": "Chưa học", "needs_review": "Cần ôn"}.get(status, status)
    return f'<span class="gm-badge {cls}">{label}</span>'


def render_module_detail():
    render_topbar()

    m = CURRENT_MODULE
    st.markdown(f"### 📦 {m['name']}")
    st.caption(f"Thời lượng: {m['duration']}")
    st.divider()

    col_left, col_right = st.columns([2, 3], gap="large")

    with col_left:
        st.markdown('<div class="gm-card">', unsafe_allow_html=True)
        st.markdown('<div class="gm-section-subtitle">Tổng quan chặng</div>', unsafe_allow_html=True)
        st.markdown(f"**Thời lượng:** {m['duration']}")
        st.markdown("**Kỹ năng đạt được:**")
        for skill in m["skills_gained"]:
            st.markdown(f"  • {skill}")
        st.divider()
        st.markdown("**Hoàn thành khi:**")
        st.caption(m["completion_criteria"])
        st.markdown('</div>', unsafe_allow_html=True)

        # CTAs
        in_progress = [l for l in m["lessons"] if l["status"] == "in_progress"]
        not_started = [l for l in m["lessons"] if l["status"] == "not_started"]

        if in_progress:
            if st.button("▶️ Tiếp tục học", type="primary", use_container_width=True):
                st.session_state["selected_screen"] = "lesson"
                st.switch_page("pages/lesson.py")
        elif not_started:
            if st.button("▶️ Học ngay", type="primary", use_container_width=True):
                st.session_state["selected_screen"] = "lesson"
                st.switch_page("pages/lesson.py")

        completed_count = sum(1 for l in m["lessons"] if l["status"] == "completed")
        if completed_count > 0:
            if st.button("🔄 Ôn lại", use_container_width=True):
                pass

    with col_right:
        st.markdown('<div class="gm-section-subtitle">Danh sách bài học</div>', unsafe_allow_html=True)

        # Group by section
        sections = {}
        for lesson in m["lessons"]:
            sections.setdefault(lesson["section"], []).append(lesson)

        for section_name, lessons in sections.items():
            st.markdown(f"**{section_name}**", help=section_name)
            for lesson in lessons:
                st.markdown(
                    f'<div class="gm-card-compact"><div class="gm-flex-between">'
                    f'<div>{_lesson_icon(lesson["type"])} <strong>{lesson["title"]}</strong><br>'
                    f'<span class="gm-text-muted gm-text-small">{lesson["duration"]} phút · '
                    f'{"Bắt buộc" if lesson["required"] else "Tùy chọn"}</span></div>'
                    f'<div>{_lesson_status(lesson["status"])}</div>'
                    f'</div></div>',
                    unsafe_allow_html=True,
                )
                if lesson["status"] in ("not_started", "in_progress"):
                    if st.button(f"Học", key=f"ml_{lesson['id']}", type="primary"):
                        st.session_state["selected_screen"] = "lesson"
                        st.switch_page("pages/lesson.py")


render_module_detail()

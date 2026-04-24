"""Screen 2 — Tạo lộ trình"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.mock_data import USER_GOAL, ROADMAP
from components.topbar import render_topbar

st.set_page_config(page_title="GenMentor — Tạo lộ trình", page_icon="🧠", layout="wide")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)


def render_create_roadmap():
    render_topbar()
    st.markdown("### 🗺️ Tạo lộ trình học tập")
    st.caption("Tất cả trong một trang — AI phân tích và tạo lộ trình cho bạn.")
    st.divider()

    col_form, col_preview = st.columns([3, 2], gap="large")

    with col_form:
        # Step 1
        with st.expander("✅ Bước 1 — Mục tiêu", expanded=True):
            st.text_input("Tôi muốn đạt gì?", value=USER_GOAL["title"], key="cr_goal")
            st.text_input("Deadline", value=USER_GOAL["deadline"], key="cr_deadline")
            st.text_input("Level hiện tại", value=USER_GOAL["current_level"], key="cr_level")

        # Step 2
        with st.expander("✅ Bước 2 — Hồ sơ / Năng lực", expanded=False):
            st.text_area("Kỹ năng hiện tại (mỗi kỹ năng một dòng)", value="React\nJavaScript\nHTML/CSS\nGit", key="cr_skills")
            uploaded = st.file_uploader("Upload CV (PDF)", type=["pdf"], key="cr_cv")
            if uploaded:
                st.success(f"✅ {uploaded.name}")

        # Step 3
        with st.expander("✅ Bước 3 — Thời gian học", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                st.number_input("Buổi / tuần", min_value=1, max_value=14, value=USER_GOAL["sessions_per_week"], key="cr_sessions")
            with c2:
                st.number_input("Phút / buổi", min_value=10, max_value=180, value=45, key="cr_minutes")
            st.multiselect(
                "Khung giờ phù hợp",
                ["Sáng sớm (6-8h)", "Buổi sáng (8-12h)", "Buổi chiều (12-17h)", "Buổi tối (18-22h)", "Cuối tuần"],
                default=["Buổi tối (18-22h)"],
                key="cr_hours",
            )

        # Step 4
        with st.expander("✅ Bước 4 — Xác nhận AI hiểu đúng", expanded=False):
            st.markdown("**Skill đã trích xuất:** React, JavaScript, HTML/CSS, Git")
            st.markdown("**Gaps phát hiện:** TypeScript, Testing, State Management, System Design")
            st.markdown("**Output dự kiến:** Senior Frontend Developer trong 24 tuần")

    with col_preview:
        st.markdown('<div class="gm-card">', unsafe_allow_html=True)
        st.markdown('<div class="gm-section-subtitle">📋 Preview lộ trình</div>', unsafe_allow_html=True)
        st.markdown(f"**Thời lượng:** {ROADMAP['total_weeks']} tuần")
        st.markdown(f"**Số chặng:** {len(ROADMAP['milestones'])}")
        st.markdown(f"**Tổng giờ ước tính:** ~72 giờ")
        st.divider()
        st.markdown("**Chặng đầu tiên:**")
        st.caption(ROADMAP["milestones"][0]["name"])
        st.caption(f"Skills: {', '.join(ROADMAP['milestones'][0]['skills'])}")
        st.divider()
        st.markdown("**Bài học đầu tiên:**")
        st.caption("Giới thiệu Redux Toolkit · 30 phút")
        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("🚀 Tạo lộ trình học", type="primary", use_container_width=True):
            st.session_state["selected_screen"] = "dashboard"
            st.success("✅ Lộ trình đã được tạo!")
            st.switch_page("pages/dashboard.py")


render_create_roadmap()

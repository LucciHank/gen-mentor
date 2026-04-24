"""Screen 8 — Review & Điều chỉnh"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.mock_data import REVIEW_DATA, PROGRESS
from components.reschedule_drawer import render_reschedule_drawer
from components.topbar import render_topbar

st.set_page_config(page_title="GenMentor — Review", page_icon="🧠", layout="wide")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)


def render_review():
    render_topbar()
    rd = REVIEW_DATA

    st.markdown("### 🔄 Review & Điều chỉnh")
    st.caption(f"Tuần {rd['week_number']}")
    st.divider()

    # Section 1 — Tuần này
    st.markdown('<div class="gm-section-title">Tuần này</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="gm-metric">', unsafe_allow_html=True)
        st.markdown(f'<div class="gm-metric-value">{rd["completion_pct"]}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="gm-metric-label">Hoàn thành</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"**Task hoàn thành:** {rd['tasks_completed']}/{rd['tasks_total']}")
    with c3:
        st.markdown("**Kỹ năng tăng:**")
        for s in rd["skills_improved"]:
            st.markdown(f"  ✅ {s}")

    if rd["slow_tasks"]:
        st.markdown("**Task chậm:**")
        for t in rd["slow_tasks"]:
            st.markdown(f"  ⚠️ {t}")

    st.divider()

    # Section 2 — AI Insight
    st.markdown('<div class="gm-section-title">🤖 AI Insight</div>', unsafe_allow_html=True)
    st.markdown('<div class="gm-card">', unsafe_allow_html=True)
    st.markdown(f"**Nguyên nhân:** {rd['ai_insight']['cause']}")
    st.divider()
    st.markdown("**Gợi ý:**")
    for i, suggestion in enumerate(rd["ai_insight"]["suggestions"], 1):
        st.markdown(f"{i}. {suggestion}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Section 3 — Điều chỉnh
    st.markdown('<div class="gm-section-title">⚙️ Điều chỉnh kế hoạch</div>', unsafe_allow_html=True)
    st.markdown('<div class="gm-card">', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.number_input("Sessions / tuần", min_value=1, max_value=14, value=5, key="rev_sessions")
    with c2:
        st.number_input("Phút / buổi", min_value=10, max_value=180, value=45, key="rev_minutes")

    st.selectbox("Pace", ["Giữ nguyên", "Giảm tải", "Tăng tốc"], key="rev_pace")

    if st.button("🔄 Regenerate path", use_container_width=True):
        st.info("Đang tạo lại lộ trình... (mock)")

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("✅ Áp dụng kế hoạch mới", type="primary", use_container_width=True):
        st.success("✅ Kế hoạch mới đã được áp dụng!")

    # Quick reschedule drawer trigger
    st.divider()
    if st.button("📅 Dời task nhanh (drawer)"):
        render_reschedule_drawer()


render_review()

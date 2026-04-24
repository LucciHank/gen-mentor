"""Screen 7 — Tiến độ / Kỹ năng"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.mock_data import PROGRESS, SKILLS, ROADMAP
from components.topbar import render_topbar

st.set_page_config(page_title="GenMentor — Tiến độ", page_icon="🧠", layout="wide")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)


def render_progress():
    render_topbar()

    st.markdown("### 📊 Tiến độ & Kỹ năng")
    st.divider()

    # Block 1 — Progress overview
    st.markdown('<div class="gm-section-title">Tiến độ tổng quan</div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown('<div class="gm-metric">', unsafe_allow_html=True)
        st.markdown(f'<div class="gm-metric-value">{PROGRESS["overall_completion"]}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="gm-metric-label">Hoàn thành roadmap</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="gm-metric">', unsafe_allow_html=True)
        st.markdown(f'<div class="gm-metric-value">{PROGRESS["weekly_velocity"]}%</div>', unsafe_allow_html=True)
        st.markdown('<div class="gm-metric-label">Velocity tuần này</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="gm-metric">', unsafe_allow_html=True)
        st.markdown(f'<div class="gm-metric-value">{PROGRESS["streak_days"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="gm-metric-label">Ngày streak 🔥</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c4:
        st.markdown('<div class="gm-metric">', unsafe_allow_html=True)
        st.markdown(f'<div class="gm-metric-value">{PROGRESS["tasks_completed"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="gm-metric-label">Task hoàn thành</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.progress(PROGRESS["overall_completion"] / 100, text=f'{PROGRESS["hours_completed"]}/{PROGRESS["hours_total"]} giờ')

    st.divider()

    # Block 2 — Skill map
    st.markdown('<div class="gm-section-title">Skill Map</div>', unsafe_allow_html=True)

    tab_have, tab_building, tab_missing = st.tabs(["✅ Đã có", "🔨 Đang xây", "❌ Còn thiếu"])

    with tab_have:
        for skill in SKILLS["mastered"]:
            _skill_row(skill)

    with tab_building:
        for skill in SKILLS["building"]:
            _skill_row(skill)

    with tab_missing:
        for skill in SKILLS["missing"]:
            _skill_row(skill)

    st.divider()

    # Block 3 — Insights
    st.markdown('<div class="gm-section-title">💡 Insight</div>', unsafe_allow_html=True)
    st.markdown('<div class="gm-card">', unsafe_allow_html=True)
    st.markdown(f"**Mạnh ở:** {PROGRESS['insights']['strength']}")
    st.markdown(f"**Đang chậm ở:** {PROGRESS['insights']['weakness']}")
    st.markdown(f"**Cần ôn lại:** Testing & async patterns")
    st.markdown('</div>', unsafe_allow_html=True)

    st.divider()

    # Block 4 — Suggested actions
    st.markdown('<div class="gm-section-title">🎯 Gợi ý hành động</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="gm-card">'
        f'{PROGRESS["insights"]["suggestion"]}<br><br>'
        '<strong>Muốn tăng kỹ năng Testing, hãy học 2 bài sau:</strong><br>'
        '• Jest cơ bản (35 phút)<br>'
        '• React Testing Library (40 phút)'
        '</div>',
        unsafe_allow_html=True,
    )
    if st.button("Học ngay", type="primary"):
        st.session_state["selected_screen"] = "lesson"
        st.switch_page("pages/lesson.py")


def _skill_row(skill):
    trend_icon = {"up": "📈", "stable": "➡️", "new": "🆕"}.get(skill["trend"], "")
    st.markdown(
        f'<div class="gm-card-compact"><div class="gm-flex-between">'
        f'<div><strong>{skill["name"]}</strong> {trend_icon}</div>'
        f'<div style="width:120px;">{skill["level"]}%</div>'
        f'</div>'
        f'<div class="gm-skill-bar-bg" style="margin-top:6px;">'
        f'<div class="gm-skill-bar-fill" style="width:{skill["level"]}%;"></div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )


render_progress()

"""Screen 3 — Roadmap"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.mock_data import ROADMAP
from components.topbar import render_topbar

st.set_page_config(page_title="GenMentor — Roadmap", page_icon="🧠", layout="wide")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)


def _milestone_status(status):
    cls = {"completed": "gm-badge-success", "in_progress": "gm-badge-primary", "not_started": "gm-badge-warning"}.get(status, "gm-badge-primary")
    label = {"completed": "Hoàn thành", "in_progress": "Đang học", "not_started": "Chờ bắt đầu"}.get(status, status)
    return f'<span class="gm-badge {cls}">{label}</span>'


def render_roadmap():
    render_topbar()

    # Header
    st.markdown(f"<h1>🗺️ {ROADMAP['name']}</h1>", unsafe_allow_html=True)
    st.markdown(f'<div style="color:var(--text-secondary); margin-bottom: 2rem;">{ROADMAP["total_weeks"]} tuần · Tuần hiện tại: {ROADMAP["current_week"]}</div>', unsafe_allow_html=True)

    # View switcher
    view = st.segmented_control("Chế độ xem", ["List", "Road"], default="List")
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    if view == "List":
        for m in ROADMAP["milestones"]:
            st.markdown('<div class="gm-card">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns([2.5, 1, 1], gap="medium")
            with c1:
                st.markdown(f"<div style='font-weight:700; font-size:18px;'>{m['name']}</div>", unsafe_allow_html=True)
                st.markdown(f"<div style='font-size:13px; color:var(--text-tertiary);'>{m['weeks']} · {', '.join(m['skills'])}</div>", unsafe_allow_html=True)
            with c2:
                st.markdown(_milestone_status(m["status"]), unsafe_allow_html=True)
            with c3:
                st.progress(m["progress"] / 100)
                st.markdown(f"<div style='font-size:11px; text-align:right; margin-top:4px;'>{m['progress']}%</div>", unsafe_allow_html=True)
            
            if m["status"] != "completed":
                st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
                if st.button("Học ngay", key=f"detail_{m['id']}", type="primary"):
                    st.session_state["selected_screen"] = "module_detail"
                    st.switch_page("pages/module_detail.py")
            st.markdown('</div>', unsafe_allow_html=True)

    else:
        # Road view
        for i, m in enumerate(ROADMAP["milestones"]):
            status_cls = {"completed": "gm-badge-success", "in_progress": "gm-badge-primary", "not_started": "gm-badge-warning"}.get(m["status"], "")
            st.markdown(
                f"""
                <div class="gm-card" style="border-left: 6px solid var(--primary);">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <div class="gm-label-caps">{m['weeks']}</div>
                            <div style="font-weight:800; font-size:20px;">{m['name']}</div>
                        </div>
                        {_milestone_status(m['status'])}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if i < len(ROADMAP["milestones"]) - 1:
                st.markdown('<div style="text-align:center; color:var(--primary); font-size:24px; margin: -12px 0 12px 0;">↓</div>', unsafe_allow_html=True)

    # Side summary
    st.divider()
    cur = ROADMAP["milestones"][1]
    st.markdown('<div class="gm-grid-3">', unsafe_allow_html=True)
    
    st.markdown(f'<div class="gm-card gm-card-compact"><div class="gm-label-caps">Tiến độ chặng</div><div style="font-size:24px; font-weight:800;">{cur["progress"]}%</div></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="gm-card gm-card-compact"><div class="gm-label-caps">Deadline</div><div style="font-size:20px; font-weight:700;">{cur["weeks"]}</div></div>', unsafe_allow_html=True)
    
    risk = "Thấp" if cur["progress"] >= 40 else "Cao"
    risk_color = "var(--success)" if risk == "Thấp" else "var(--danger)"
    st.markdown(f'<div class="gm-card gm-card-compact"><div class="gm-label-caps">Rủi ro</div><div style="font-size:24px; font-weight:800; color:{risk_color};">{risk}</div></div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


render_roadmap()

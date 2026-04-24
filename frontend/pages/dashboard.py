"""Screen 1 — Dashboard / Hôm nay"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.mock_data import USER_PROFILE, USER_GOAL, TODAY_TASKS, PROGRESS, ROADMAP
from components.floating_planner import render_floating_planner
from components.reschedule_drawer import render_reschedule_drawer
from components.topbar import render_topbar

st.set_page_config(page_title="GenMentor — Hôm nay", page_icon="🧠", layout="wide")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)


def _icon_for_type(t):
    return {"video": "🎬", "reading": "📖", "quiz": "📝", "practice": "💻", "review": "🔄"}.get(t, "📌")


def _status_badge(status):
    cls = {
        "completed": "gm-badge-success",
        "in_progress": "gm-badge-primary",
        "not_started": "gm-badge-primary",
        "overdue": "gm-badge-danger",
        "pending": "gm-badge-primary",
    }.get(status, "gm-badge-primary")
    label = {
        "completed": "Hoàn thành",
        "in_progress": "Đang học",
        "not_started": "Chưa học",
        "overdue": "Quá hạn",
        "pending": "Chờ làm",
    }.get(status, status)
    return f'<span class="gm-badge {cls}">{label}</span>'


def render_dashboard():
    render_topbar()

    name = USER_PROFILE["name"]
    goal = USER_GOAL["title"]
    week = ROADMAP["current_week"]
    total_weeks = ROADMAP["total_weeks"]

    st.markdown(f'<h1>Chào buổi chiều, {name.split()[-1]}! 👋</h1>', unsafe_allow_html=True)
    st.markdown(f'<div style="color:var(--text-secondary); margin-bottom: 2rem;">Lộ trình hiện tại: <strong>{goal}</strong></div>', unsafe_allow_html=True)

    col_main, col_side = st.columns([1.8, 1], gap="large")

    with col_main:
        # Main Daily Goal Card
        st.markdown('<div class="gm-card">', unsafe_allow_html=True)
        st.markdown('<div class="gm-label-caps">✨ Mục tiêu hôm nay</div>', unsafe_allow_html=True)
        
        total_min = sum(t["duration"] for t in TODAY_TASKS)
        completed = sum(1 for t in TODAY_TASKS if t["status"] == "completed")
        pct = int(completed / len(TODAY_TASKS) * 100) if TODAY_TASKS else 0
        
        st.markdown(f'<div style="font-size:40px; font-weight:800; letter-spacing:-0.05em; margin-bottom:12px;">{total_min} phút <span style="font-size:18px; font-weight:500; color:var(--text-tertiary); letter-spacing:0;">{completed}/{len(TODAY_TASKS)} task</span></div>', unsafe_allow_html=True)
        
        st.progress(pct / 100)
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

        for task in TODAY_TASKS:
            icon = _icon_for_type(task["type"])
            status_html = _status_badge(task["status"])
            
            st.markdown(f"""
            <div class="gm-item">
                <div class="gm-item-icon">{icon}</div>
                <div style="flex-grow:1;">
                    <div style="font-weight:600; font-size:16px;">{task['title']}</div>
                    <div style="font-size:13px; color:var(--text-tertiary);">🕒 {task['duration']} phút</div>
                </div>
                <div>{status_html}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        if st.button("Học tiếp bài đang dở", type="primary", use_container_width=True):
            st.session_state["selected_screen"] = "lesson"
            st.switch_page("pages/lesson.py")
            
        st.markdown('<div style="text-align:center; font-size:13px; color:var(--text-tertiary); margin-top:16px; cursor:pointer; font-weight:600;">XEM TOÀN BỘ KẾ HOẠCH ›</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Learning status card
        st.markdown(f"""
        <div class="gm-card gm-card-compact" style="display:flex; align-items:center; justify-content:space-between; background-color: var(--primary-bg); border-color: rgba(0,122,255,0.1);">
            <div style="display:flex; align-items:center; gap:16px;">
                <div style="font-size:24px; color: var(--primary);">📘</div>
                <div>
                    <div class="gm-label-caps" style="color:var(--primary); margin-bottom:2px;">Đang học dở</div>
                    <div style="font-weight:700; color: var(--text-primary);">MODULE 2 / LESSON 4: ADVANCED REACT HOOKS</div>
                </div>
            </div>
            <div style="background:var(--primary); color:white; padding:8px 16px; border-radius:12px; font-weight:700; font-size:12px;">
                08:21 / 24:00
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Next Best Action
        st.markdown(f"""
        <div class="gm-alert gm-alert-warning">
            <div style="font-size:24px;">💡</div>
            <div style="flex-grow:1;">
                <div class="gm-label-caps" style="color:#B45309;">Gợi ý hành động</div>
                <div style="font-size:14px; font-weight:500;">Hoàn thành quiz sau video để mở khóa bài thực hành quan trọng.</div>
            </div>
            <div style="font-size:20px; color:#B45309;">→</div>
        </div>
        """, unsafe_allow_html=True)

    with col_side:
        # Goal/Target Card
        st.markdown('<div class="gm-card">', unsafe_allow_html=True)
        st.markdown('<div style="display:flex; align-items:center; gap:12px; margin-bottom:24px;">', unsafe_allow_html=True)
        st.markdown('<div style="background:var(--primary); color:white; width:44px; height:44px; border-radius:14px; display:flex; align-items:center; justify-content:center; font-size:22px; box-shadow: 0 4px 12px rgba(0,122,255,0.3);">🚀</div>', unsafe_allow_html=True)
        st.markdown('<div><div class="gm-label-caps">Mục tiêu của bạn</div><div style="font-weight:800; font-size:16px; letter-spacing:-0.02em;">SENIOR FRONTEND</div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown('<div class="gm-label-caps">Hoàn thành</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:28px; font-weight:800;">{PROGRESS["overall_completion"]}%</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="gm-label-caps">Lộ trình</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:28px; font-weight:800;">{total_weeks} tuần</div>', unsafe_allow_html=True)
        
        hr = '<hr>'
        st.markdown(hr, unsafe_allow_html=True)
        st.markdown(f"🔥 Streak hiện tại: **{PROGRESS['streak_days']} ngày**")
        st.markdown(f"🏁 Milestone: <span style='color:var(--primary); font-weight:700;'>{PROGRESS['next_milestone']}</span>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Warning Card
        if PROGRESS["weekly_velocity"] < 80:
            st.markdown(f"""
            <div class="gm-alert gm-alert-danger">
                <div style="flex-grow:1;">
                    <div class="gm-label-caps" style="color:var(--danger);">Cảnh báo tiến độ</div>
                    <div style="font-size:14px; font-weight:600; color:#991B1B; margin-bottom:12px;">Bạn đang chậm 2 task so với kế hoạch ban đầu.</div>
            """, unsafe_allow_html=True)
            if st.button("BẮT KỊP NGAY", key="catchup_btn", use_container_width=True, type="primary"):
                st.switch_page("pages/weekly_plan.py")
            st.markdown('</div>', unsafe_allow_html=True)

        # Weekly Progress Card
        st.markdown('<div class="gm-card">', unsafe_allow_html=True)
        st.markdown('<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">', unsafe_allow_html=True)
        st.markdown('<div><div style="font-weight:800; font-size:18px;">Tuần này</div><div class="gm-label-caps">TUẦN {0} / {1}</div></div>'.format(week, total_weeks), unsafe_allow_html=True)
        st.markdown('<div style="background:rgba(52, 199, 89, 0.1); color:var(--success); padding:6px; border-radius:10px; font-size:18px;">📈</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown(f'<div style="font-size:32px; font-weight:800; margin-bottom:8px;">{PROGRESS["weekly_completion"]}%</div>', unsafe_allow_html=True)
        st.progress(PROGRESS["weekly_completion"] / 100)
        
        st.markdown('<div style="margin-top: 1.5rem;"></div>', unsafe_allow_html=True)
        st.markdown('<div class="gm-label-caps">Kỹ năng đạt được</div>', unsafe_allow_html=True)
        for skill in PROGRESS["skills_gained_this_week"][:2]:
            st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; font-size:14px; margin-bottom:8px;">
                <div style="font-weight:500;">{skill}</div>
                <div style="color:var(--success); font-weight:700;">LEVEL UP</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    render_floating_planner()


render_dashboard()

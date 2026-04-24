"""Screen 6 — Task / Kế hoạch tuần"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.mock_data import WEEKLY_PLAN
from components.reschedule_drawer import render_reschedule_drawer
from components.topbar import render_topbar

st.set_page_config(page_title="GenMentor — Kế hoạch tuần", page_icon="🧠", layout="wide")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)


def _task_icon(t):
    return {"video": "🎬", "reading": "📖", "quiz": "📝", "practice": "💻", "review": "🔄", "overdue": "⚠️", "completed": "✅"}.get(t, "📌")


def _task_status_badge(status):
    cls = {"completed": "gm-badge-completed", "in_progress": "gm-badge-in-progress", "pending": "gm-badge-not-started", "overdue": "gm-badge-overdue"}.get(status, "gm-badge-not-started")
    label = {"completed": "Xong", "in_progress": "Đang học", "pending": "Chờ làm", "overdue": "Quá hạn"}.get(status, status)
    return f'<span class="gm-badge {cls}">{label}</span>'


def render_weekly_plan():
    render_topbar()

    wp = WEEKLY_PLAN
    st.markdown(f"### 📋 Tuần {wp['week_number']} / {wp['phase']}")
    st.caption(f"Tổng giờ học tuần này: ~{wp['total_hours']}h")
    st.divider()

    # Tabs
    tabs = st.tabs(["Hôm nay", "Tuần này", "Quá hạn", "Hoàn thành"])

    # Filter tasks
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    today_tasks = [t for t in wp["tasks"] if t["date"] == today and t["status"] not in ("completed", "overdue")]
    week_tasks = [t for t in wp["tasks"] if t["status"] not in ("completed", "overdue")]
    overdue_tasks = [t for t in wp["tasks"] if t["status"] == "overdue"]
    completed_tasks = [t for t in wp["tasks"] if t["status"] == "completed"]

    with tabs[0]:
        if not today_tasks:
            st.info("Không có task nào cho hôm nay. 🎉")
        else:
            for task in today_tasks:
                _render_task_card(task)

    with tabs[1]:
        for task in week_tasks:
            _render_task_card(task)

    with tabs[2]:
        if not overdue_tasks:
            st.success("Không có task quá hạn! 🎉")
        else:
            for task in overdue_tasks:
                _render_task_card(task, show_reschedule=True)

    with tabs[3]:
        for task in completed_tasks:
            _render_task_card(task)


def _render_task_card(task, show_reschedule=False):
    st.markdown(
        f'<div class="gm-card-compact"><div class="gm-flex-between">'
        f'<div>{_task_icon(task["type"])} <strong>{task["title"]}</strong><br>'
        f'<span class="gm-text-muted gm-text-small">{task["module"]} · {task["duration"]} phút · '
        f'{"Bắt buộc" if task["required"] else "Tùy chọn"}</span></div>'
        f'<div>{_task_status_badge(task["status"])}</div>'
        f'</div></div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns([1, 1, 1])
    with c1:
        if task["status"] in ("pending", "in_progress"):
            if st.button("Bắt đầu", key=f"wp_start_{task['id']}", type="primary", use_container_width=True):
                st.session_state["selected_screen"] = "lesson"
                st.switch_page("pages/lesson.py")
    with c2:
        if task["status"] != "completed":
            if st.button("Dời lịch", key=f"wp_resched_{task['id']}", use_container_width=True):
                render_reschedule_drawer(task)
    with c3:
        if task["status"] != "completed":
            if st.button("Đánh dấu xong", key=f"wp_done_{task['id']}", use_container_width=True):
                st.success(f"✅ Đã hoàn thành: {task['title']}")


render_weekly_plan()

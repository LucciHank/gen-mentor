import streamlit as st
import time
from utils.state import initialize_session_state, save_persistent_state

initialize_session_state()

st.set_page_config(page_title="GenMentor", page_icon="🧠", layout="wide")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)

# ── Auto-navigate after onboarding ──────────────────────────
if st.session_state.get("if_complete_onboarding", False):
    try:
        st.switch_page("pages/dashboard.py")
    except Exception:
        pass

# ── Navigation ──────────────────────────────────────────────
if not st.session_state.get("if_complete_onboarding", False):
    # Before onboarding complete — only show onboarding
    pg = st.navigation([
        st.Page("pages/onboarding.py", title="Chào mừng", icon=":material/how_to_reg:", default=True, url_path="onboarding"),
    ])
else:
    # After onboarding — full app with 8 screens
    dashboard = st.Page("pages/dashboard.py", title="Hôm nay", icon=":material/home:", default=True, url_path="dashboard")
    roadmap = st.Page("pages/roadmap.py", title="Roadmap", icon=":material/route:", url_path="roadmap")
    progress = st.Page("pages/progress.py", title="Tiến độ", icon=":material/insights:", url_path="progress")
    review = st.Page("pages/review.py", title="Điều chỉnh", icon=":material/settings:", url_path="review")
    create_roadmap = st.Page("pages/create_roadmap.py", title="Tạo lộ trình", icon=":material/add_circle:", url_path="create_roadmap")
    module_detail = st.Page("pages/module_detail.py", title="Chi tiết chặng", icon=":material/folder:", url_path="module_detail")
    lesson = st.Page("pages/lesson.py", title="Bài học", icon=":material/play_circle:", url_path="lesson")
    weekly_plan = st.Page("pages/weekly_plan.py", title="Kế hoạch tuần", icon=":material/calendar_today:", url_path="weekly_plan")

    pg = st.navigation({
        "Trang chủ": [dashboard],
        "Lộ trình của tôi": [dashboard, roadmap, progress, review],
        "Khóa học của tôi": [module_detail, lesson],
        "Bài tập": [weekly_plan],
        "Khám phá": [create_roadmap],
    }, position="sidebar")

    # Sidebar Branding
    with st.sidebar:
        st.markdown("""
        <div style="padding: 10px 0 24px 0; display:flex; align-items:center; gap:12px;">
            <div style="background:var(--primary); width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:800; font-size:18px;">G</div>
            <div style="font-size:20px; font-weight:800; letter-spacing:-0.04em;">GenMentor</div>
        </div>
        """, unsafe_allow_html=True)

    # Sidebar reset button
    with st.sidebar:
        st.divider()
        if st.button("🔄 Thiết lập lại", key="reset_btn", use_container_width=True):
            from utils.state import reset_onboarding
            reset_onboarding()
            st.switch_page("pages/onboarding.py")
        
        st.markdown("""
        <div style="margin-top: 20px; font-size:13px; color:var(--text-tertiary); display:flex; align-items:center; gap:8px; cursor:pointer;">
            <span>❓ Giúp đỡ</span>
        </div>
        """, unsafe_allow_html=True)

pg.run()

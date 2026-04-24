import streamlit as st
import time
from utils.state import complete_onboarding, save_persistent_state

st.set_page_config(page_title="GenMentor", page_icon="🧠", layout="wide")
st.markdown('<style>' + open('./assets/css/main.css').read() + '</style>', unsafe_allow_html=True)


def _init_onboarding():
    for key in ["ob_goal_desire", "ob_goal_specific", "ob_sessions", "ob_minutes", "ob_cv"]:
        st.session_state.setdefault(key, None)


def render_onboarding():
    _init_onboarding()

    # ── Hero ──────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center; padding: 4rem 0 3rem 0;">
            <div style="background:var(--primary); width:64px; height:64px; border-radius:16px; display:inline-flex; align-items:center; justify-content:center; color:white; font-size:32px; margin-bottom:1.5rem; box-shadow: 0 10px 30px rgba(0,122,255,0.3);">🧠</div>
            <h1 style="font-size: 48px; margin-bottom: 0.5rem;">Chào mừng đến với GenMentor</h1>
            <p style="font-size: 18px; color: var(--text-secondary); max-width: 600px; margin: 0 auto;">AI kiến tạo lộ trình học tập cá nhân hóa dựa trên mục tiêu và hồ sơ năng lực của riêng bạn.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Form ──────────────────────────────────────────────
    col_left, col_right = st.columns([1.8, 1], gap="large")

    with col_left:
        st.markdown('<div class="gm-card">', unsafe_allow_html=True)
        st.markdown('<div class="gm-label-caps">🎯 Mục tiêu học tập</div>', unsafe_allow_html=True)

        desire = st.text_input(
            "Mục tiêu lớn nhất của bạn là gì?",
            placeholder="VD: Trở thành Senior Frontend Developer trong 6 tháng tới...",
            key="ob_goal_desire",
            label_visibility="collapsed"
        )

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown('<div class="gm-label-caps">Chức danh cụ thể</div>', unsafe_allow_html=True)
        specific = st.text_input(
            "Vị trí công việc cụ thể",
            placeholder="VD: Senior Frontend Developer",
            key="ob_goal_specific",
            label_visibility="collapsed"
        )

        st.markdown('<hr>', unsafe_allow_html=True)
        st.markdown('<div class="gm-label-caps">⏰ Quỹ thời gian cam kết</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            sessions = st.number_input(
                "Số buổi học / tuần",
                min_value=1,
                max_value=14,
                value=5,
                step=1,
                key="ob_sessions",
            )
        with col_b:
            minutes = st.number_input(
                "Số phút / buổi",
                min_value=10,
                max_value=180,
                value=45,
                step=5,
                key="ob_minutes",
            )

        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="gm-card">', unsafe_allow_html=True)
        st.markdown('<div class="gm-label-caps">📄 Hồ sơ năng lực</div>', unsafe_allow_html=True)
        st.markdown("<div style='font-size: 14px; color: var(--text-secondary); margin-bottom: 1rem;'>Tải CV của bạn lên để AI phân tích khoảng cách kỹ năng (Skill Gap) chính xác hơn.</div>", unsafe_allow_html=True)

        cv_file = st.file_uploader(
            "Upload CV (PDF)",
            type=["pdf"],
            key="ob_cv",
            label_visibility="collapsed",
        )

        if cv_file:
            st.markdown(f'<div class="gm-badge gm-badge-success">✅ Đã tải lên: {cv_file.name}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_right:
        # ── Preview panel ─────────────────────────────────
        st.markdown('<div class="gm-card" style="background-color: white; border: 2px solid var(--primary-bg);">', unsafe_allow_html=True)
        st.markdown('<div class="gm-label-caps" style="color:var(--primary);">📋 Preview lộ trình</div>', unsafe_allow_html=True)
        
        if desire:
            st.markdown(f"<div style='font-weight:700; font-size:18px; margin-bottom:12px;'>{desire}</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='font-weight:700; font-size:18px; color:var(--text-tertiary); margin-bottom:12px;'>Chưa nhập mục tiêu...</div>", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:var(--bg); border-radius:12px; padding:16px;">
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:var(--text-secondary); font-size:14px;">Thời lượng:</span>
                <span style="font-weight:600; font-size:14px;">{sessions} buổi/tuần</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="color:var(--text-secondary); font-size:14px;">Thời gian học:</span>
                <span style="font-weight:600; font-size:14px;">{minutes} phút/buổi</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        total_hours = (sessions * minutes * 24) / 60
        st.markdown(f"""
        <div style="margin-top: 1.5rem; text-align:center;">
            <div style="font-size:13px; color:var(--text-tertiary);">Ước tính thời gian học</div>
            <div style="font-size:32px; font-weight:800; color:var(--primary);">~{total_hours:.0f} giờ</div>
            <div style="font-size:13px; color:var(--text-tertiary);">trong vòng 24 tuần</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("🚀 Tạo lộ trình ngay", type="primary", use_container_width=True):
            if not desire or not specific:
                st.warning("Vui lòng điền thông tin mục tiêu.")
            else:
                with st.spinner("🤖 AI đang phân tích hồ sơ và tạo lộ trình..."):
                    time.sleep(3)
                data = {
                    "desire": desire,
                    "specific": specific,
                    "sessions_per_week": sessions,
                    "minutes_per_session": minutes,
                    "cv_uploaded": cv_file is not None,
                    "cv_name": cv_file.name if cv_file else None,
                }
                complete_onboarding(data)
                st.switch_page("pages/dashboard.py")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("""
        <div style="padding: 0 12px; font-size:12px; color:var(--text-tertiary); text-align:center;">
            Bằng cách bắt đầu, bạn đồng ý với Điều khoản sử dụng của GenMentor.
        </div>
        """, unsafe_allow_html=True)


render_onboarding()

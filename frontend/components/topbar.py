"""Topbar — simplified for mock mode with notification panel"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from components.notifications import render_notifications


def render_topbar():
    """Premium topbar with search and profile icons."""
    st.markdown("""
    <div style="display:flex; justify-content:space-between; align-items:center; padding: 12px 0; margin-bottom: 24px;">
        <div style="display:flex; align-items:center; gap:8px;">
            <div style="background:linear-gradient(135deg, #2D63ED 0%, #1D4ED8 100%); width:32px; height:32px; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-weight:800; font-size:18px;">G</div>
            <div style="font-size:20px; font-weight:800; letter-spacing:-0.03em;">GenMentor</div>
        </div>
        <div style="display:flex; align-items:center; gap:20px;">
            <div style="color:var(--text-tertiary); font-size:18px; cursor:pointer;">🔍</div>
            <div style="color:var(--text-tertiary); font-size:18px; cursor:pointer; position:relative;">
                🔔
                <div style="position:absolute; top:-2px; right:-2px; width:8px; height:8px; background:var(--danger); border-radius:50%; border:2px solid white;"></div>
            </div>
            <div style="display:flex; align-items:center; gap:8px; background:white; padding:4px 12px; border-radius:20px; border:1px solid var(--border); cursor:pointer;">
                <div style="width:24px; height:24px; border-radius:50%; background:#E5E7EB; display:flex; align-items:center; justify-content:center; font-size:12px;">👤</div>
                <div style="font-size:13px; font-weight:600;">Admin</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_topbar_with_settings():
    """Topbar with settings button for backend config."""
    col_left, col_center, col_right = st.columns([1, 5, 2])

    with col_center:
        st.markdown(
            '<div style="font-size:18px;font-weight:700;color:var(--primary);">🧠 GenMentor</div>',
            unsafe_allow_html=True,
        )

    with col_right:
        from assets.mock_data import NOTIFICATIONS
        unread = sum(1 for n in NOTIFICATIONS if not n["read"])
        notif_label = f"🔔 {unread}" if unread else "🔔"
        if st.button(notif_label, key="topbar_notif", use_container_width=False):
            render_notifications()

        if st.button("⚙️", key="topbar_settings", use_container_width=False):
            _settings_dialog()


@st.dialog("Cài đặt")
def _settings_dialog():
    st.markdown("**Cài đặt**")
    st.info("Mock mode đang bật — không cần backend.")
    if st.button("Đóng", use_container_width=True):
        st.rerun()

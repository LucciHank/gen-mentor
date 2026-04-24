"""UI Layer E — Notification Panel"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.mock_data import NOTIFICATIONS


def render_notifications():
    """Notification panel — opens from topbar."""
    st.markdown("### 🔔 Thông báo")
    st.divider()

    unread = sum(1 for n in NOTIFICATIONS if not n["read"])
    st.caption(f"{unread} thông báo chưa đọc")
    st.divider()

    for notif in NOTIFICATIONS:
        icon = {"task": "📋", "alert": "⚠️", "milestone": "🏆", "reminder": "⏰"}.get(notif["type"], "📌")
        dot = '<span class="gm-notif-dot"></span>' if not notif["read"] else ""
        st.markdown(
            f'<div class="gm-card-compact">'
            f'<div class="gm-flex-between">'
            f'<div>{icon} <strong>{notif["title"]}</strong> {dot}<br>'
            f'<span class="gm-text-muted gm-text-small">{notif["message"]}</span></div>'
            f'<div><span class="gm-text-muted gm-text-small">{notif["time"]}</span></div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

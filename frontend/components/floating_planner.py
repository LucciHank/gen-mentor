"""UI Layer A — Floating Mini Planner"""
import streamlit as st
import sys
import os

# Add the frontend directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from assets.mock_data import TODAY_TASKS


def render_floating_planner():
    """Collapsible floating widget showing remaining tasks and next action."""
    remaining = [t for t in TODAY_TASKS if t["status"] in ("pending", "in_progress")]
    total_min = sum(t["duration"] for t in remaining)

    # Use a dialog-like floating card at bottom of page
    st.markdown("---")
    with st.expander("📌 Mini Planner", expanded=False):
        if not remaining:
            st.success("🎉 Hoàn thành tất cả task hôm nay!")
        else:
            st.markdown(f"**{len(remaining)} task còn lại** · ~{total_min} phút")
            for t in remaining[:3]:
                st.markdown(f"• {t['title']} ({t['duration']} phút)")

            if remaining:
                next_task = remaining[0]
                st.divider()
                st.markdown(f"**Tiếp theo:** {next_task['title']}")
                c1, c2 = st.columns(2)
                with c1:
                    if st.button("Tiếp tục", key="fp_continue", use_container_width=True, type="primary"):
                        st.session_state["selected_screen"] = "lesson"
                        st.switch_page("pages/lesson.py")
                with c2:
                    if st.button("Dời lịch", key="fp_reschedule", use_container_width=True):
                        st.info("Mở reschedule drawer...")

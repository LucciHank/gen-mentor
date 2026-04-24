"""UI Layer B — AI Coach Side Panel"""
import streamlit as st


def render_ai_coach(lesson):
    """Contextual AI coach panel with 4 tabs for lesson/module screens."""
    st.markdown('<div class="gm-card">', unsafe_allow_html=True)
    st.markdown('<div class="gm-section-subtitle">🤖 AI Coach</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Mục tiêu", "Checklist", "Ghi chú", "Tiếp theo"])

    with tabs[0]:
        st.markdown("**Mục tiêu bài học:**")
        for obj in lesson.get("objectives", []):
            st.markdown(f"• {obj}")
        st.divider()
        st.caption(f"⏱ ~{lesson.get('duration', 30)} phút")

    with tabs[1]:
        st.markdown("**Checklist:**")
        for item in lesson.get("checklist", []):
            st.checkbox(item, key=f"check_{item[:20]}")

    with tabs[2]:
        st.markdown("**Ghi chú của bạn:**")
        notes = st.text_area("", key="coach_notes", height=120, label_visibility="collapsed", placeholder="Note nhanh, bookmark đoạn chưa hiểu...")
        if notes:
            st.session_state.setdefault("lesson_notes_list", []).append(notes)

    with tabs[3]:
        st.markdown("**Sau bài học:**")
        st.markdown("• Làm quiz kiểm tra")
        st.markdown("• Học bài kế tiếp")
        st.markdown("• Nếu điểm thấp → ôn lại")
        st.divider()
        if st.button("Làm quiz", use_container_width=True, type="primary"):
            st.info("Starting quiz...")

    st.markdown('</div>', unsafe_allow_html=True)

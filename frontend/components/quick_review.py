"""UI Layer D — Quick Review Sheet"""
import streamlit as st


def render_quick_review():
    """Post-lesson/quiz review sheet — understanding level, next steps."""
    st.markdown("### 📝 Quick Review")
    st.divider()

    st.markdown("**Bạn hiểu bài này ở mức nào?**")
    level = st.radio("", ["Thấp — Cần ôn lại", "Vừa — Hiểu cơ bản", "Tốt — Sẵn sàng bài tiếp"], key="review_level", horizontal=True)

    st.divider()

    if "Thấp" in level:
        st.warning("💡 Gợi ý: Ôn lại bài này trước khi tiếp tục.")
        if st.button("Ôn lại", type="primary"):
            st.info("Đang mở lại bài học...")
    elif "Vừa" in level:
        st.info("💡 Gợi ý: Làm quiz để củng cố kiến thức.")
        if st.button("Làm quiz", type="primary"):
            st.info("Starting quiz...")
    else:
        st.success("💡 Tuyệt vời! Bạn đã sẵn sàng học bài tiếp theo.")
        if st.button("Học tiếp", type="primary"):
            st.session_state["selected_screen"] = "module_detail"
            st.switch_page("pages/module_detail.py")

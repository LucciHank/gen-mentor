"""UI Layer C — Reschedule Drawer"""
import streamlit as st
from datetime import datetime, timedelta


def render_reschedule_drawer(task=None):
    """Drawer/dialog for rescheduling tasks."""
    task_name = task["title"] if task else "task"

    st.markdown(f"**Dời lịch:** {task_name}")
    st.divider()

    option = st.radio(
        "Chọn phương án:",
        ["Dời sang ngày khác", "Giảm tải tuần này", "Học 20 phút/ngày", "Skip task tùy chọn"],
        key="reschedule_option",
    )

    if option == "Dời sang ngày khác":
        new_date = st.date_input("Chọn ngày mới", value=datetime.now() + timedelta(days=1), key="reschedule_date")
        if st.button("Xác nhận dời lịch", type="primary", use_container_width=True):
            st.success(f"✅ Đã dời '{task_name}' sang {new_date.strftime('%d/%m/%Y')}")

    elif option == "Giảm tải tuần này":
        st.caption("Giảm 1-2 task optional trong tuần này")
        if st.button("Áp dụng giảm tải", type="primary", use_container_width=True):
            st.success("✅ Đã giảm tải tuần này")

    elif option == "Học 20 phút/ngày":
        st.caption("Chia nhỏ task thành session 20 phút")
        if st.button("Áp dụng", type="primary", use_container_width=True):
            st.success("✅ Đã chia nhỏ task thành session 20 phút")

    elif option == "Skip task tùy chọn":
        st.caption("Bỏ qua task không bắt buộc")
        if st.button("Skip task này", type="primary", use_container_width=True):
            st.success(f"✅ Đã skip '{task_name}'")

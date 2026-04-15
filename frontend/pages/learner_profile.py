import math
import streamlit as st
from utils.request_api import create_learner_profile, update_learner_profile
from components.skill_info import render_skill_info
from components.navigation import render_navigation
from utils.pdf import extract_text_from_pdf
from streamlit_extras.tags import tagger_component 
from utils.state import save_persistent_state


def render_learner_profile():
    # Title and introduction
    goal = st.session_state["goals"][st.session_state["selected_goal_id"]]

    st.title("Hồ sơ người học")
    st.write("Tổng quan về lý lịch, mục tiêu, tiến độ, sở thích và các mẫu hành vi của người học.")
    if not goal["learner_profile"]:
        with st.spinner('Đang xác định lỗ hổng kỹ năng ...'):
            st.info("Vui lòng hoàn thành quá trình khởi đầu để xem hồ sơ người học.")
    else:
        try:
            render_learner_profile_info(goal)
        except Exception as e:
            st.error("Đã xảy ra lỗi khi hiển thị hồ sơ người học.")
            # re generate the learner profile
            with st.spinner("Đang chuẩn bị lại hồ sơ của bạn ..."):
                learner_profile = create_learner_profile(goal["learning_goal"], st.session_state["learner_information"], goal["skill_gaps"], st.session_state["llm_type"])
            goal["learner_profile"] = learner_profile
            try:
                save_persistent_state()
            except Exception:
                pass
            st.rerun()

def render_learner_profile_info(goal):
    st.markdown("""
        <style>
        .section {
            background-color: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 8px;
        }
        .progress-indicator {
            color: #28a745;
            font-weight: bold;
        }
        .skill-in-progress {
            color: #ffc107;
        }
        .skill-required {
            color: #dc3545;
        }
        </style>
    """, unsafe_allow_html=True)
    learner_profile = goal["learner_profile"]
    with st.container(border=True):
        # Learner Information
        st.markdown("#### 👤 Thông tin người học")
        st.markdown(f"<div class='section'>{learner_profile['learner_information']}</div>", unsafe_allow_html=True)

        # Learning Goal
        st.markdown("#### 🎯 Mục tiêu học tập")
        st.markdown(f"<div class='section'>{learner_profile['learning_goal']}</div>", unsafe_allow_html=True)

    with st.container(border=True):
        render_cognitive_status(goal)
    with st.container(border=True):
        render_learning_preferences(goal)
    with st.container(border=True):
        render_behavioral_patterns(goal)

    render_additional_info_form(goal)


def render_cognitive_status(goal):
    learner_profile = goal["learner_profile"]
    # Cognitive Status
    st.markdown("#### 🧠 Trạng thái nhận thức")
    st.write("**Tiến độ tổng thể:**")
    st.progress(learner_profile["cognitive_status"]["overall_progress"])
    st.markdown(f"<p class='progress-indicator'>{learner_profile['cognitive_status']['overall_progress']}% đã hoàn thành</p>", unsafe_allow_html=True)
    render_skill_info(learner_profile)

def render_learning_preferences(goal):
    learner_profile = goal["learner_profile"]
    st.markdown("#### 📚 Sở thích học tập")
    st.write(f"**Phong cách nội dung:** {learner_profile['learning_preferences']['content_style']}")
    st.write(f"**Loại hoạt động ưa thích:** {learner_profile['learning_preferences']['activity_type']}")
    st.write(f"**Ghi chú bổ sung:**")
    st.info(learner_profile['learning_preferences']['additional_notes'])

def render_behavioral_patterns(goal):
    learner_profile = goal["learner_profile"]
    st.markdown("#### 📊 Các mẫu hành vi")
    st.write(f"**Tần suất sử dụng hệ thống:**")
    st.info(learner_profile['behavioral_patterns']['system_usage_frequency'])
    st.write(f"**Thời lượng buổi học và sự tham gia:**")
    st.info(learner_profile['behavioral_patterns']['session_duration_engagement'])
    st.write(f"**Các yếu tố thúc đẩy động lực:**")
    st.info(learner_profile['behavioral_patterns']['motivational_triggers'])
    st.write(f"**Ghi chú bổ sung:**")
    st.info(learner_profile['behavioral_patterns']['additional_notes'])


def render_additional_info_form(goal):
    with st.form(key="additional_info_form"):
        st.markdown("#### Đánh giá của bạn")
        st.info("Hãy giúp chúng tôi cải thiện trải nghiệm học tập của bạn bằng cách cung cấp phản hồi dưới đây.")
        st.write("Bạn đồng ý bao nhiêu phần trăm với hồ sơ hiện tại?")
        agreement_star = st.feedback("stars", key="agreement_star")
        st.write("Bạn có đề xuất hoặc chỉnh sửa nào không?")
        suggestions = st.text_area("Cung cấp đề xuất của bạn tại đây.", label_visibility="collapsed")
        st.write("Bạn có thêm thông tin nào muốn bổ sung không?")
        additional_info = st.text_area("Cung cấp thêm thông tin hoặc phản hồi tại đây.", label_visibility="collapsed")
        pdf_file = st.file_uploader("Tải lên tệp PDF có thông tin bổ sung (ví dụ: CV)", type="pdf")
        if pdf_file is not None:
            with st.spinner("Đang trích xuất văn bản từ PDF..."):
                additional_info_pdf = extract_text_from_pdf(pdf_file)
                st.toast("✅ PDF đã được tải lên thành công.")
        else:
            additional_info_pdf = ""
        st.session_state["additional_info"] = {
            "agreement_star": agreement_star,
            "suggestions": suggestions,
            "additional_info": additional_info + additional_info_pdf
        }
        try:
            save_persistent_state()
        except Exception:
            pass
        submit_button = st.form_submit_button("Cập nhật hồ sơ", on_click=update_learner_profile_with_additional_info, 
                                              kwargs={"goal": goal, "additional_info": additional_info, }, type="primary")
        
def update_learner_profile_with_additional_info(goal, additional_info):
    additional_info = st.session_state["additional_info"]
    new_learner_profile = update_learner_profile(goal["learner_profile"], additional_info)
    if new_learner_profile is not None:
        goal["learner_profile"] = new_learner_profile
        try:
            save_persistent_state()
        except Exception:
            pass
        st.toast("🎉 Đã cập nhật hồ sơ của bạn thành công!")
    else:
        st.toast("❌ Cập nhật hồ sơ thất bại. Vui lòng thử lại.")


render_learner_profile()
import streamlit as st

import time
import asyncio
from components.goal_refinement import render_goal_refinement
from utils.pdf import extract_text_from_pdf
from utils.state import save_persistent_state
from components.topbar import render_topbar


def on_refine_click():
    st.session_state["if_refining_learning_goal"] = True
    try:
        save_persistent_state()
    except Exception:
        pass


def _init_onboarding_state():
    """Ensure required session_state keys exist to avoid KeyErrors."""
    st.session_state.setdefault("onboarding_card_index", 0)  # 0: goal, 1: info
    st.session_state.setdefault("if_refining_learning_goal", False)
    st.session_state.setdefault("learner_occupation", "")
    st.session_state.setdefault("learner_information_text", "")
    st.session_state.setdefault("learner_information", "")
    st.session_state.setdefault("to_add_goal", {"learning_goal": ""})
    try:
        save_persistent_state()
    except Exception:
        pass


def _inject_card_css():
    """Inject lightweight CSS to make sections look like cards and style nav buttons."""
    st.markdown(
        """
        <style>
        .gm-card { 
            background: #ffffff; 
            border: 1px solid rgba(0,0,0,0.08);
            border-radius: 14px; 
            box-shadow: 0 8px 24px rgba(0,0,0,0.06);
            padding: 24px 22px; 
        }
        .gm-side { position: sticky; top: 160px; }
        .gm-side .gm-side-btn {
            border: 1px solid rgba(0,0,0,0.12);
            background: #ffffff;
            color: #111827;
            padding: 6px 10px; 
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
            font-weight: 700;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

def render_onboard():
    _init_onboarding_state()
    _inject_card_css()
    left, center, right = st.columns([1, 5, 1])
    goal = st.session_state["to_add_goal"]
    if "refined_learning_goal" not in st.session_state:
        st.session_state["refined_learning_goal"] = goal["learning_goal"]
        try:
            save_persistent_state()
        except Exception:
            pass
    with center:
        render_topbar()
        st.title("Chào mừng đến với GenMentor")
        st.write("Bắt đầu hành trình học tập cá nhân hóa và hướng mục tiêu của bạn!")
        render_cards_with_nav(goal)
        

def render_goal(goal):
    idx = st.session_state.get("onboarding_card_index", 0)
    with st.container(border=True):
        st.subheader("Thiết lập mục tiêu học tập")
        st.info("🚀 Vui lòng nhập vai trò và mục tiêu học tập cụ thể của bạn. Bạn cũng có thể tinh chỉnh nó với các gợi ý từ AI.")
        learning_goal = st.text_area("* Nhập mục tiêu học tập của bạn", value=goal["learning_goal"], label_visibility="visible", disabled=st.session_state["if_refining_learning_goal"])
        goal["learning_goal"] = learning_goal
        button_col, hint_col, next_col = st.columns([3, 10, 3])
        render_goal_refinement(goal, button_col, hint_col)
        save_persistent_state()
        with hint_col:
            if st.session_state["if_refining_learning_goal"]:
                st.write("**✨ Đang tinh chỉnh mục tiêu học tập...**")
        with next_col:
            if st.button("Tiếp theo", key="gm_nav_next", use_container_width=True, disabled=(idx == 1), type="primary"):
                st.session_state["onboarding_card_index"] = min(1, idx + 1)
                try:
                    save_persistent_state()
                except Exception:
                    pass
                st.rerun()
        



def render_information(goal):
    idx = st.session_state.get("onboarding_card_index", 0)
    with st.container(border=True):
        st.subheader("Chia sẻ thông tin của bạn")
        st.info("🧠 Vui lòng cung cấp thông tin của bạn (Văn bản hoặc PDF) để tăng cường trải nghiệm cá nhân hóa")

        occupations = ["Kỹ sư phần mềm", "Nhà khoa học dữ liệu", "Nhà nghiên cứu AI", "Quản lý sản phẩm", "Nhà thiết kế UI/UX", "Khác"]
        try:
            occupation_selectbox_index = occupations.index(st.session_state["learner_occupation"]) 
        except ValueError:
            occupation_selectbox_index = None
        ocp_left, ocp_right = st.columns([1, 1])
        with ocp_left:
            selected_occupation = st.selectbox("Chọn nghề nghiệp của bạn", occupations, index=occupation_selectbox_index)
        if selected_occupation == "Khác":
            with ocp_right:
                other_occupation = st.text_input("Vui lòng ghi rõ nghề nghiệp của bạn")
            if other_occupation:
                st.session_state["learner_occupation"] = other_occupation
                try:
                    save_persistent_state()
                except Exception:
                    pass
        if selected_occupation is None:
            st.session_state["learner_occupation"] = ""
            try:
                save_persistent_state()
            except Exception:
                pass
        else:
            st.session_state["learner_occupation"] = selected_occupation
            try:
                save_persistent_state()
            except Exception:
                pass
        upload_col, information_col = st.columns([1, 1])
        with upload_col:
            uploaded_file = st.file_uploader("[Tùy chọn] Tải lên tệp PDF thông tin của bạn (ví dụ: CV)", type="pdf")
            if uploaded_file is not None:
                with st.spinner("Đang trích xuất văn bản từ PDF..."):
                    learner_information_pdf = extract_text_from_pdf(uploaded_file)
                    st.toast("✅ PDF đã được tải lên thành công.")
            else:
                learner_information_pdf = ""
        with information_col:
            learner_information_text = st.text_area("[Tùy chọn] Nhập sở thích và phong cách học tập của bạn", value=st.session_state["learner_information_text"], label_visibility="visible", height=77)
            st.session_state["learner_information"] = st.session_state["learner_occupation"] + learner_information_text + learner_information_pdf
            try:
                save_persistent_state()
            except Exception:
                pass
        # st.divider()
        arrow_left, space_col, continue_button_col = st.columns([3, 10, 3])
        save_persistent_state()
        with arrow_left:
            if st.button("Quay lại", key="gm_nav_prev", use_container_width=True, disabled=(idx == 0)):
                st.session_state["onboarding_card_index"] = max(0, idx - 1)
                try:
                    save_persistent_state()
                except Exception:
                    pass
                st.rerun()
        with continue_button_col:
            render_continue_button(goal)

def render_continue_button(goal):
    if st.button("Lưu & Tiếp tục", type="primary"):
        if not goal["learning_goal"] or not st.session_state["learner_occupation"]:
            st.warning("Vui lòng cung cấp cả mục tiêu học tập và nghề nghiệp của bạn trước khi tiếp tục.")
        else:
            st.session_state["selected_page"] = "Skill Gap"
            try:
                save_persistent_state()
            except Exception:
                pass
            st.switch_page("pages/skill_gap.py")


def render_cards_with_nav(goal):
    """Show either the Goal or Information section as a card with left/center/right nav buttons."""
    idx = st.session_state.get("onboarding_card_index", 0)

    if idx == 0:
        render_goal(goal)
    else:
        render_information(goal)

render_onboard()
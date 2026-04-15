import streamlit as st

from components.goal_refinement import render_goal_refinement
from utils.request_api import create_learner_profile, identify_skill_gap
from components.gap_identification import render_identified_skill_gap, render_identifying_skill_gap
from utils.state import add_new_goal, change_selected_goal_id, index_goal_by_id, reset_to_add_goal, save_persistent_state
from components.skill_info import render_skill_info


def render_goal_management():
    st.title("Quản lý mục tiêu")
    st.write("Quản lý các mục tiêu học tập của bạn: thêm mới, chỉnh sửa hoặc xóa các mục tiêu hiện có.")

    render_add_new_goal()
    st.divider()
    render_existing_goals()

def render_add_new_goal():
    if "if_refining_learning_goal" not in st.session_state:
        st.session_state["if_refining_learning_goal"] = False
        try:
            save_persistent_state()
        except Exception:
            pass
    if "if_show_skill_gap_results_in_dialog" not in st.session_state:
        st.session_state["if_show_skill_gap_results_in_dialog"] = False
        try:
            save_persistent_state()
        except Exception:
            pass

    to_add_goal = st.session_state["to_add_goal"]
    st.subheader("🎯 Thêm mục tiêu mới")
    new_learning_goal = st.text_area("Nhập mục tiêu mới của bạn:", to_add_goal["learning_goal"], key="new_learning_goal")
    to_add_goal["learning_goal"] = new_learning_goal

    refine_col, clear_col, hint_col, add_col = st.columns([1, 1, 3, 1])

    render_goal_refinement(to_add_goal, refine_col, hint_col)
    if clear_col.button("Xóa", key="clear_goal"):
        reset_to_add_goal()
        try:
            save_persistent_state()
        except Exception:
            pass
        st.rerun()

    if add_col.button("Thêm mục tiêu", type="primary", icon=":material/add:", use_container_width=True):
        if new_learning_goal:
            render_skill_gap_dialog()
        else:
            hint_col.warning("Vui lòng nhập mục tiêu trước khi thêm.")

    if st.session_state["if_show_skill_gap_results_in_dialog"]:
        render_skill_gap_dialog()



def render_existing_goals():
    st.subheader("📋 Các mục tiêu hiện có")
    goals = st.session_state["goals"]
    non_deleted_goals = [goal for goal in goals if not goal["is_deleted"]]

    for goal_id, goal in enumerate(non_deleted_goals):
        with st.container():
            col_left, col_right = st.columns([3, 1])
            col_left.write(f"#### Mục tiêu {goal_id + 1}")
            
            # Check if the current goal is the active goal
            is_active = st.session_state.get("selected_goal_id") == goal["id"]
            
            if is_active:
                col_right.button("Mục tiêu đang hoạt động", type="primary", key=f"active_{goal['id']}", use_container_width=True)
            else:
                if col_right.button("Đặt làm mục tiêu chính", key=f"set_{goal['id']}", help="Đánh dấu mục tiêu này là mục tiêu học tập chính của bạn."):
                    st.session_state.selected_goal_id = goal["id"]
                    try:
                        save_persistent_state()
                    except Exception:
                        pass
                    change_selected_goal_id(goal["id"])
                    try:
                        save_persistent_state()
                    except Exception:
                        pass
                    st.rerun()
            
            st.info(f"{goal['learning_goal']}")
            st.write(f"**Tiến độ tổng thể:**")
            learner_profile = goal["learner_profile"]
            overall_progress = learner_profile["cognitive_status"]["overall_progress"]
            progress = st.slider("Tiến độ", min_value=0, max_value=100, value=overall_progress, key=f"progress_{goal['id']}", disabled=True)
            unlearned_skill = len(goal['learner_profile']['cognitive_status']['in_progress_skills'])
            learned_skill = len(goal['learner_profile']['cognitive_status']['mastered_skills'])
            all_skill = learned_skill + unlearned_skill
            col1, col2, col3 = st.columns([1, 1, 1])
            with col1:
                st.metric(label="Tổng số kỹ năng", value=all_skill, delta_color="off")
            with col2:
                st.metric(label="Kỹ năng đã thành thạo", value=learned_skill, delta_color="off")
            with col3:
                st.metric(label="Kỹ năng đang học", value=unlearned_skill, delta_color="off")
            with st.expander("Thông tin kỹ năng"):
                render_skill_info(goal["learner_profile"])
            
            col1, col2 = st.columns([7, 1])
            with col1:
                if st.button("Sửa", key=f"edit_{goal['id']}"):
                    edited_goal = st.text_area("Sửa mục tiêu", value=goal["learning_goal"])
                    if st.button("Lưu", key=f"save_{goal['id']}"):
                        goal["learning_goal"] = edited_goal
                        st.success("Cập nhật mục tiêu thành công!")
            with col2:
                if st.button("Xóa", key=f"delete_{goal['id']}", type="primary"):
                    goal_index = index_goal_by_id(goal["id"])
                    st.session_state.goals[goal_index]["is_deleted"] = True
                    try:
                        save_persistent_state()
                    except Exception:
                        pass
                    st.success("Đã xóa mục tiêu thành công!")
                    st.rerun()
        
        if goal_id < len(non_deleted_goals) - 1:
            st.divider()

            
            


@st.dialog("Lỗ hổng kỹ năng", width="large")
def render_skill_gap_dialog():
    to_add_goal = st.session_state["to_add_goal"]
    st.write("Xem lại và xác nhận các lỗ hổng kỹ năng của bạn.")
    num_skills = len(to_add_goal["skill_gaps"])
    num_gaps = sum(1 for skill in to_add_goal["skill_gaps"] if skill["is_gap"])
    st.info(f"Có tổng cộng {num_skills} kỹ năng, với {num_gaps} lỗ hổng kỹ năng được xác định.")
    if not to_add_goal["skill_gaps"]:
        st.session_state["if_show_skill_gap_results_in_dialog"] = True
        try:
            save_persistent_state()
        except Exception:
            pass
        render_identifying_skill_gap(to_add_goal)
    else:
        st.session_state["if_show_skill_gap_results_in_dialog"] = False
        try:
            save_persistent_state()
        except Exception:
            pass
        render_identified_skill_gap(to_add_goal)
        if_schedule_learning_path_ready = to_add_goal["skill_gaps"]
        if st.button("Lập lộ trình học tập", type="primary", disabled=not if_schedule_learning_path_ready):
            if to_add_goal["skill_gaps"] and not to_add_goal["learner_profile"]:
                with st.spinner('Đang tạo hồ sơ của bạn ...'):
                    learner_profile = create_learner_profile(to_add_goal["learning_goal"], st.session_state["learner_information"], to_add_goal["skill_gaps"])
                    if learner_profile is None:
                        st.rerun()
                    to_add_goal["learner_profile"] = learner_profile
                    st.toast("🎉 Hồ sơ của bạn đã được tạo!")
            new_goal_id = add_new_goal(**to_add_goal)
            st.session_state["selected_goal_id"] = new_goal_id
            try:
                save_persistent_state()
            except Exception:
                pass
            st.session_state["if_complete_onboarding"] = True
            try:
                save_persistent_state()
            except Exception:
                pass
            st.session_state["selected_page"] = "Learning Path"
            try:
                save_persistent_state()
            except Exception:
                pass
            st.switch_page("pages/learning_path.py")



render_goal_management()
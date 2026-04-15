import streamlit as st

from utils.request_api import create_learner_profile, identify_skill_gap
from utils.state import save_persistent_state

def render_identifying_skill_gap(goal):
    with st.spinner('Đang xác định lỗ hổng kỹ năng ...'):
        learning_goal = goal["learning_goal"]
        learner_information = st.session_state["learner_information"]
        llm_type = st.session_state["llm_type"]
        skill_gaps = identify_skill_gap(learning_goal, learner_information, llm_type)
    goal["skill_gaps"] = skill_gaps
    save_persistent_state()
    st.rerun()
    st.toast("🎉 Xác định lỗ hổng kỹ năng thành công!")
    return skill_gaps


def render_identified_skill_gap(goal, method_name="genmentor"):
    """
    Render skill gaps in a card-style with prev/next switching.
    """
    levels = ["Chưa học", "Sơ cấp", "Trung cấp", "Cao cấp"]
    # Render all skill cards on a single page (no pagination)
    skill_gaps = goal.get("skill_gaps", [])
    total = len(skill_gaps)
    if total == 0:
        st.info("Chưa có kỹ năng nào được xác định.")
        return

    from utils.translation import translate_level, get_level_key, translate_confidence
    for skill_id, skill_info in enumerate(skill_gaps):
        skill_name = skill_info.get("name", f"skill_{skill_id}")
        required_level_key = skill_info.get("required_level", "unlearned")
        current_level_key = skill_info.get("current_level", "unlearned")
        
        # Map English keys to Vietnamese for display
        required_level_display = translate_level(required_level_key)
        current_level_display = translate_level(current_level_key)

        background_color = "#ffe6e6" if skill_info.get("is_gap") else "#e6ffe6"
        text_color = "#ff4d4d" if skill_info.get("is_gap") else "#33cc33"

        with st.container(border=True):
            # Card header
            st.markdown(
                f"""
                <div style="background-color: {background_color}; color: {text_color}; padding: 10px 16px; border-radius: 8px; margin-bottom: 12px; display: flex; align-items: center; min-height: 44px;">
                    <p style="font-weight: 700; margin: 0; flex: 1;">{skill_id+1:2d}. {skill_name}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Required level selector
            new_required_level_display = st.pills(
                "**Mức độ yêu cầu**",
                options=levels,
                selection_mode="single",
                default=required_level_display,
                disabled=False,
                key=f"required_{skill_name}_{method_name}",
            )
            new_required_level_key = get_level_key(new_required_level_display)
            if new_required_level_key != required_level_key:
                goal["skill_gaps"][skill_id]["required_level"] = new_required_level_key
                
                # Internal logic uses English keys or order of levels list
                # Since levels list is in Vietnamese, we should use get_level_key to compare via order
                eng_levels = ["unlearned", "beginner", "intermediate", "advanced"]
                if eng_levels.index(new_required_level_key) > eng_levels.index(goal["skill_gaps"][skill_id].get("current_level", "unlearned")):
                    goal["skill_gaps"][skill_id]["is_gap"] = True
                else:
                    goal["skill_gaps"][skill_id]["is_gap"] = False
                save_persistent_state()
                st.rerun()

            # Current level selector
            new_current_level_display = st.pills(
                "**Mức độ hiện tại**",
                options=levels,
                selection_mode="single",
                default=current_level_display,
                disabled=False,
                key=f"current_{skill_name}__{method_name}",
            )
            new_current_level_key = get_level_key(new_current_level_display)
            if new_current_level_key != current_level_key:
                goal["skill_gaps"][skill_id]["current_level"] = new_current_level_key
                eng_levels = ["unlearned", "beginner", "intermediate", "advanced"]
                if eng_levels.index(new_current_level_key) < eng_levels.index(goal["skill_gaps"][skill_id].get("required_level", "unlearned")):
                    goal["skill_gaps"][skill_id]["is_gap"] = True
                else:
                    goal["skill_gaps"][skill_id]["is_gap"] = False
                save_persistent_state()
                st.rerun()

            # Details
            with st.expander("Chi tiết phân tích thêm"):
                eng_levels = ["unlearned", "beginner", "intermediate", "advanced"]
                if eng_levels.index(goal["skill_gaps"][skill_id].get("current_level", "unlearned")) < eng_levels.index(goal["skill_gaps"][skill_id].get("required_level", "unlearned")):
                    st.warning("Mức độ hiện tại thấp hơn mức độ yêu cầu!")
                    goal["skill_gaps"][skill_id]["is_gap"] = True
                else:
                    st.success("Mức độ hiện tại bằng hoặc cao hơn yêu cầu")
                    goal["skill_gaps"][skill_id]["is_gap"] = False
                st.write(f"**Lý do**: {skill_info.get('reason', '')}")
                st.write(f"**Mức độ tin cậy**: {translate_confidence(skill_info.get('level_confidence', ''))}")
            save_persistent_state()
            # Gap toggle
            old_gap_status = skill_info.get("is_gap", False)
            gap_status = st.toggle(
                "Đánh dấu là lỗ hổng",
                value=skill_info.get("is_gap", False),
                key=f"gap_{skill_name}_{method_name}",
                disabled=not skill_info.get("is_gap", False),
            )
            if gap_status != old_gap_status:
                goal["skill_gaps"][skill_id]["is_gap"] = gap_status
                if not goal["skill_gaps"][skill_id]["is_gap"]:
                    goal["skill_gaps"][skill_id]["current_level"] = goal["skill_gaps"][skill_id].get("required_level", goal["skill_gaps"][skill_id].get("current_level"))
                try:
                    save_persistent_state()
                except Exception:
                    pass
                st.rerun()


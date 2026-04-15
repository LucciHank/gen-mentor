import streamlit as st
from collections import defaultdict
import pandas as pd
import re
import time

from utils.state import get_current_session_uid

def render_dashboard():
    goal = st.session_state["goals"][st.session_state["selected_goal_id"]]

    if not goal["learner_profile"]:
        st.warning("Vui lòng chờ lộ trình học tập được lập để xem bảng điều khiển.")

    st.title("Phân tích học tập")
    st.write("Theo dõi tiến trình học tập và xem các phân tích học tập tại đây.")
    with st.container(border=True):
        render_learning_progress(goal)
    with st.container(border=True):
        render_skill_radar_chart(goal)
    with st.container(border=True):
        render_session_learning_timeseries(goal)
    with st.container(border=True):
        render_mastery_skills_timeseries(goal)


def render_learning_progress(goal):
    st.markdown("#### Tiến trình học tập")
    st.write("Xem tiến trình học tập cho từng buổi học.")
    learner_profile = goal["learner_profile"]
    overall_progress = learner_profile["cognitive_status"]["overall_progress"]
    st.progress(overall_progress)
    st.write(f"Tiến độ tổng quát: {overall_progress:.2f}%")

def render_skill_radar_chart(goal):
    import plotly.graph_objects as go

    st.markdown("#### Mức độ thành thạo các kỹ năng")
    # st.write("View the skill radar chart for your learning progress.")
    learner_profile = goal["learner_profile"]
    mastered_skills = learner_profile["cognitive_status"]["mastered_skills"]
    in_progress_skills = learner_profile["cognitive_status"]["in_progress_skills"]
    level_map = defaultdict(lambda: 0, {"unlearned": 0, "beginner": 1, "intermediate": 2, "advanced": 3})
    mastered_skills = [{
        "name": skill_info["name"], 
        "required_level": skill_info["proficiency_level"], 
        "current_level": skill_info["proficiency_level"]} for skill_info in mastered_skills]
    in_progress_skills = [{
        "name": skill_info["name"], 
        "required_level": skill_info["required_proficiency_level"], 
        "current_level": skill_info["current_proficiency_level"]} for skill_info in in_progress_skills]
    skills = mastered_skills + in_progress_skills
    skill_names = [skill["name"] for skill in skills]
    current_levels = [level_map[skill["current_level"]] for skill in skills]
    required_levels = [level_map[skill["required_level"]] for skill in skills]
    st.write(f"Bạn đã thành thạo {len(mastered_skills)} kỹ năng và đang học {len(in_progress_skills)} kỹ năng.")

    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=current_levels,
        theta=skill_names,
        fill='toself',
        name='Mức độ thành thạo hiện tại',
    ))
    fig.add_trace(go.Scatterpolar(
        r=required_levels,
        theta=skill_names,
        fill='toself',
        name='Mức độ thành thạo yêu cầu',
        fillcolor='rgba(255, 192, 203, 0.3)',
        line=dict(color='rgba(255, 105, 97, 0.6)')
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 3],
                tickvals=[0, 1, 2, 3],
                ticktext=['Chưa học', 'Sơ cấp', 'Trung cấp', 'Cao cấp'],
                tickfont=dict(size=14)
            ),
            angularaxis=dict(  # Set font size for skill names (theta labels)
                tickfont=dict(size=18)
            )
        ),
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5,
            font=dict(size=18)
        ),
    )
    event = st.plotly_chart(fig, key="iris", on_select="rerun")


def render_session_learning_timeseries(goal):
    st.markdown("#### Chuỗi thời gian học tập theo buổi")
    st.write("Xem tiến trình học tập theo thời gian.")
    goal = st.session_state["goals"][st.session_state["selected_goal_id"]]
    session_data = {
        "Session": [],
        "Time": [],
    }
    for session in goal["learning_path"]:
        session_data["Session"].append(session['id'])
        if_learned = session['if_learned']
        
        if if_learned:
            selected_gid = st.session_state["selected_goal_id"]
            match = re.search(r'\d+', session['id'])
            selected_sid = int(match.group(0)) -1
            times = st.session_state["session_learning_times"][f'{selected_gid}-{selected_sid}']
            if times["end_time"] is not None:
                # st.markdown(times)
                time_spent = (times["end_time"] - times["start_time"]) / 60
                # st.markdown(time_spent)
            else:  
                time_spent = 0
            session_data["Time"].append(time_spent)
            # st.markdown(session_data)
        else:
            session_data["Time"].append(0)
    
    for sid, session in enumerate(goal["learning_path"]):
        session_uid = session["id"]
        if session_uid not in session_data["Session"]:
            session_data["Session"].append(session_uid)
            session_data["Time"].append(0)

    session_data = pd.DataFrame(session_data)

    st.bar_chart(session_data, x="Session", y="Time", stack=False)
    

def render_mastery_skills_timeseries(goal):
    st.markdown("#### Chuỗi thời gian thành thạo kỹ năng")
    st.write("Xem tiến trình học tập theo thời gian.")
    time_values = [i * 10 for i in range(len(st.session_state['learned_skills_history'][goal['id']]))]
    char_data = pd.DataFrame({
        'Mastery Rate': st.session_state['learned_skills_history'][goal['id']],
        'Time': time_values,
    })
    st.line_chart(char_data, x='Time', y='Mastery Rate')
    


render_dashboard()

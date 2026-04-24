import streamlit as st
from collections import defaultdict
import config
import json
from pathlib import Path

PERSIST_KEYS = [
    "backend_endpoint",
    "if_complete_onboarding",
    "selected_screen",
    "mock_user",
    "mock_goal",
    "mock_roadmap",
    "mock_module",
    "mock_weekly_plan",
    "mock_skills",
    "mock_progress",
    "mock_notifications",
    "mock_review",
    "onboarding_data",
    "goals",
    "selected_goal_id",
    "userId",
    "show_notifications",
]


def _get_data_store_path():
    return Path(__file__).resolve().parents[1] / "user_data" / "data_store.json"


def load_persistent_state():
    path = _get_data_store_path()
    if not path.exists():
        return False
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return False
    for k, v in data.items():
        if k in PERSIST_KEYS:
            st.session_state[k] = v
    return True


def save_persistent_state():
    path = _get_data_store_path()
    data = {}
    for k in PERSIST_KEYS:
        if k in st.session_state:
            try:
                data[k] = st.session_state[k]
            except Exception:
                pass
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except Exception:
        return False


def initialize_session_state():
    defaults = {
        "if_complete_onboarding": False,
        "selected_screen": "dashboard",
        "userId": "TestUser",
        "show_notifications": False,
        "goals": [],
        "selected_goal_id": 0,
        "onboarding_data": {},
        "mock_user": None,
        "mock_goal": None,
        "mock_roadmap": None,
        "mock_module": None,
        "mock_weekly_plan": None,
        "mock_skills": None,
        "mock_progress": None,
        "mock_notifications": None,
        "mock_review": None,
        "backend_endpoint": config.backend_endpoint,
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

    try:
        load_persistent_state()
    except Exception:
        pass


def reset_onboarding():
    """Clear onboarding state for fresh start."""
    st.session_state["if_complete_onboarding"] = False
    st.session_state["onboarding_data"] = {}
    try:
        save_persistent_state()
    except Exception:
        pass


def complete_onboarding(data):
    """Mark onboarding complete and store user data."""
    st.session_state["if_complete_onboarding"] = True
    st.session_state["onboarding_data"] = data
    st.session_state["selected_screen"] = "dashboard"
    try:
        save_persistent_state()
    except Exception:
        pass


def get_current_goal():
    """Get the active learning goal."""
    return st.session_state.get("mock_goal") or st.session_state.get("onboarding_data", {}).get("goal")

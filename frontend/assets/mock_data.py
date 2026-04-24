"""Mock data for GenMentor UI — all screens work without backend."""

from datetime import datetime, timedelta

# ── User Profile ──────────────────────────────────────────────
USER_PROFILE = {
    "name": "Nguyễn Văn An",
    "email": "an.nguyen@example.com",
    "role": "student",  # student | employee | new_hire
    "avatar": "./assets/avatar.png",
}

# ── Goal ──────────────────────────────────────────────────────
USER_GOAL = {
    "title": "Senior Frontend Developer",
    "category": "Software Engineering",
    "deadline": "2026-12-31",
    "current_level": "Mid-level (3 năm kinh nghiệm)",
    "sessions_per_week": 5,
    "minutes_per_session": 45,
}

# ── Roadmap ───────────────────────────────────────────────────
ROADMAP = {
    "name": "Lộ trình Senior Frontend Developer",
    "total_weeks": 24,
    "current_week": 4,
    "status": "on_track",  # on_track | behind | ahead
    "milestones": [
        {
            "id": "m1",
            "name": "Chặng 1 — Nền tảng React nâng cao",
            "weeks": "Tuần 1–6",
            "duration": "6 tuần",
            "skills": ["React Hooks", "Context API", "Performance Optimization"],
            "status": "completed",
            "progress": 100,
        },
        {
            "id": "m2",
            "name": "Chặng 2 — State Management & Testing",
            "weeks": "Tuần 7–12",
            "duration": "6 tuần",
            "skills": ["Redux Toolkit", "Zustand", "Jest", "React Testing Library"],
            "status": "in_progress",
            "progress": 45,
        },
        {
            "id": "m3",
            "name": "Chặng 3 — TypeScript & Architecture",
            "weeks": "Tuần 13–18",
            "duration": "6 tuần",
            "skills": ["TypeScript Advanced", "Design Patterns", "Clean Architecture"],
            "status": "not_started",
            "progress": 0,
        },
        {
            "id": "m4",
            "name": "Chặng 4 — System Design & Leadership",
            "weeks": "Tuần 19–24",
            "duration": "6 tuần",
            "skills": ["Micro Frontend", "Monorepo", "Code Review", "Mentoring"],
            "status": "not_started",
            "progress": 0,
        },
    ],
}

# ── Current Module (Chặng 2) ─────────────────────────────────
CURRENT_MODULE = {
    "id": "m2",
    "name": "State Management & Testing",
    "duration": "6 tuần",
    "skills_gained": ["Redux Toolkit", "Zustand", "Jest", "React Testing Library"],
    "completion_criteria": "Hoàn thành 8 bài học + 4 quiz + 1 project cuối chặng",
    "lessons": [
        {
            "id": "l1",
            "title": "Giới thiệu Redux Toolkit",
            "type": "video",
            "duration": 30,
            "required": True,
            "status": "completed",
            "section": "Redux Toolkit",
        },
        {
            "id": "l2",
            "title": "CreateSlice & Reducers",
            "type": "video",
            "duration": 45,
            "required": True,
            "status": "completed",
            "section": "Redux Toolkit",
        },
        {
            "id": "l3",
            "title": "Async Thunks & RTK Query",
            "type": "video",
            "duration": 50,
            "required": True,
            "status": "in_progress",
            "section": "Redux Toolkit",
        },
        {
            "id": "l4",
            "title": "Quiz: Redux Toolkit",
            "type": "quiz",
            "duration": 20,
            "required": True,
            "status": "not_started",
            "section": "Redux Toolkit",
        },
        {
            "id": "l5",
            "title": "Zustand — State đơn giản hơn",
            "type": "reading",
            "duration": 25,
            "required": True,
            "status": "not_started",
            "section": "Zustand",
        },
        {
            "id": "l6",
            "title": "So sánh Zustand vs Redux",
            "type": "practice",
            "duration": 40,
            "required": False,
            "status": "not_started",
            "section": "Zustand",
        },
        {
            "id": "l7",
            "title": "Jest cơ bản",
            "type": "video",
            "duration": 35,
            "required": True,
            "status": "not_started",
            "section": "Testing",
        },
        {
            "id": "l8",
            "title": "React Testing Library",
            "type": "video",
            "duration": 40,
            "required": True,
            "status": "not_started",
            "section": "Testing",
        },
    ],
}

# ── Weekly Tasks ──────────────────────────────────────────────
def _generate_weekly_tasks():
    today = datetime.now()
    return {
        "week_number": 4,
        "phase": "Chặng 2",
        "total_hours": 6.5,
        "tasks": [
            {
                "id": "t1",
                "type": "video",
                "title": "Async Thunks & RTK Query",
                "duration": 50,
                "required": True,
                "status": "in_progress",
                "date": (today - timedelta(days=1)).strftime("%Y-%m-%d"),
                "module": "Redux Toolkit",
            },
            {
                "id": "t2",
                "type": "quiz",
                "title": "Quiz: Redux Toolkit",
                "duration": 20,
                "required": True,
                "status": "pending",
                "date": today.strftime("%Y-%m-%d"),
                "module": "Redux Toolkit",
            },
            {
                "id": "t3",
                "type": "reading",
                "title": "Zustand — State đơn giản hơn",
                "duration": 25,
                "required": True,
                "status": "pending",
                "date": today.strftime("%Y-%m-%d"),
                "module": "Zustand",
            },
            {
                "id": "t4",
                "type": "practice",
                "title": "So sánh Zustand vs Redux",
                "duration": 40,
                "required": False,
                "status": "pending",
                "date": (today + timedelta(days=1)).strftime("%Y-%m-%d"),
                "module": "Zustand",
            },
            {
                "id": "t5",
                "type": "video",
                "title": "Jest cơ bản",
                "duration": 35,
                "required": True,
                "status": "pending",
                "date": (today + timedelta(days=2)).strftime("%Y-%m-%d"),
                "module": "Testing",
            },
            {
                "id": "t6",
                "type": "overdue",
                "title": "Ôn lại CreateSlice",
                "duration": 15,
                "required": True,
                "status": "overdue",
                "date": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
                "module": "Redux Toolkit",
            },
            {
                "id": "t7",
                "type": "completed",
                "title": "Giới thiệu Redux Toolkit",
                "duration": 30,
                "required": True,
                "status": "completed",
                "date": (today - timedelta(days=4)).strftime("%Y-%m-%d"),
                "module": "Redux Toolkit",
            },
            {
                "id": "t8",
                "type": "completed",
                "title": "CreateSlice & Reducers",
                "duration": 45,
                "required": True,
                "status": "completed",
                "date": (today - timedelta(days=3)).strftime("%Y-%m-%d"),
                "module": "Redux Toolkit",
            },
        ],
    }


WEEKLY_PLAN = _generate_weekly_tasks()

# ── Skills ────────────────────────────────────────────────────
SKILLS = {
    "mastered": [
        {"name": "HTML/CSS", "level": 90, "trend": "stable"},
        {"name": "JavaScript", "level": 85, "trend": "up"},
        {"name": "React Hooks", "level": 80, "trend": "up"},
        {"name": "Git", "level": 75, "trend": "stable"},
    ],
    "building": [
        {"name": "Redux Toolkit", "level": 45, "trend": "up"},
        {"name": "TypeScript", "level": 50, "trend": "up"},
        {"name": "Testing (Jest)", "level": 30, "trend": "up"},
        {"name": "Zustand", "level": 20, "trend": "new"},
    ],
    "missing": [
        {"name": "Micro Frontend", "level": 0, "trend": "new"},
        {"name": "Monorepo (Turborepo)", "level": 0, "trend": "new"},
        {"name": "System Design", "level": 10, "trend": "new"},
        {"name": "Mentoring", "level": 15, "trend": "new"},
    ],
}

# ── Progress ──────────────────────────────────────────────────
PROGRESS = {
    "overall_completion": 18,
    "weekly_velocity": 72,  # percent of weekly target
    "streak_days": 12,
    "tasks_completed": 14,
    "tasks_total": 78,
    "hours_completed": 12.5,
    "hours_total": 72,
    "next_milestone": "Chặng 3 — TypeScript & Architecture",
    "next_milestone_eta": "Tuần 13",
    "skills_gained_this_week": ["Redux Toolkit (+15%)"],
    "weekly_completion": 65,
    "slow_tasks": ["Ôn lại CreateSlice"],
    "insights": {
        "strength": "React Hooks & JavaScript nền tảng vững",
        "weakness": "Testing & async patterns cần ôn lại",
        "suggestion": "Dành thêm 15 phút/ngày cho quiz & practice",
    },
}

# ── Today's Tasks (for Dashboard) ────────────────────────────
def _generate_today_tasks():
    today = datetime.now()
    return [
        {
            "id": "td1",
            "title": "Quiz: Redux Toolkit",
            "type": "quiz",
            "duration": 20,
            "status": "pending",
        },
        {
            "id": "td2",
            "title": "Zustand — State đơn giản hơn",
            "type": "reading",
            "duration": 25,
            "status": "pending",
        },
        {
            "id": "td3",
            "title": "Ôn lại CreateSlice (quá hạn)",
            "type": "review",
            "duration": 15,
            "status": "overdue",
        },
    ]


TODAY_TASKS = _generate_today_tasks()

# ── Notifications ─────────────────────────────────────────────
NOTIFICATIONS = [
    {
        "id": "n1",
        "type": "task",
        "title": "Quiz: Redux Toolkit",
        "message": "Bài quiz hôm nay chưa hoàn thành",
        "time": "2 giờ trước",
        "read": False,
    },
    {
        "id": "n2",
        "type": "alert",
        "title": "Chậm kế hoạch",
        "message": "Bạn đang chậm 2 task so với lộ trình",
        "time": "1 ngày trước",
        "read": False,
    },
    {
        "id": "n3",
        "type": "milestone",
        "title": "Chặng 1 hoàn thành! 🎉",
        "message": "Bạn đã hoàn thành Nền tảng React nâng cao",
        "time": "3 ngày trước",
        "read": True,
    },
    {
        "id": "n4",
        "type": "reminder",
        "title": "Review cuối tuần",
        "message": "Đã đến lúc review tuần 4 — điều chỉnh kế hoạch nếu cần",
        "time": "5 giờ trước",
        "read": False,
    },
]

# ── Lesson Content (for Lesson screen) ────────────────────────
LESSON_CONTENT = {
    "id": "l3",
    "title": "Async Thunks & RTK Query",
    "type": "video",
    "duration": 50,
    "module": "Redux Toolkit",
    "objectives": [
        "Hiểu cách Redux Toolkit xử lý async operations",
        "Sử dụng createAsyncThunk để fetch data",
        "Áp dụng RTK Query cho API calls",
    ],
    "checklist": [
        "createAsyncThunk hoạt động như thế nào?",
        "Extra reducers là gì?",
        "RTK Query khác gì so với axios + thunk?",
    ],
    "transcript": """
Trong bài học này, chúng ta sẽ tìm hiểu về Async Thunks và RTK Query — hai công cụ mạnh mẽ trong Redux Toolkit để xử lý các tác vụ bất đồng bộ.

## 1. Async Thunks

createAsyncThunk là một helper function giúp tạo async action creators. Nó tự động dispatch pending/fulfilled/rejected actions.

```javascript
import { createAsyncThunk } from '@reduxjs/toolkit'

export const fetchUser = createAsyncThunk(
  'users/fetchById',
  async (userId, thunkAPI) => {
    const response = await fetch(`/api/users/${userId}`)
    return response.json()
  }
)
```

## 2. RTK Query

RTK Query là một công cụ mạnh mẽ cho data fetching và caching. Nó tự động generate hooks, loading states, và error handling.

```javascript
import { createApi, fetchBaseQuery } from '@reduxjs/toolkit/query/react'

export const api = createApi({
  reducerPath: 'api',
  baseQuery: fetchBaseQuery({ baseUrl: '/api' }),
  endpoints: (builder) => ({
    getUser: builder.query({
      query: (id) => `users/${id}`,
    }),
  }),
})
```
    """.strip(),
    "notes": [],
}

# ── Review Data ───────────────────────────────────────────────
REVIEW_DATA = {
    "week_number": 4,
    "completion_pct": 65,
    "tasks_completed": 5,
    "tasks_total": 8,
    "skills_improved": ["Redux Toolkit (+15%)", "TypeScript (+5%)"],
    "slow_tasks": ["Ôn lại CreateSlice", "Quiz: Redux Toolkit"],
    "ai_insight": {
        "cause": "Thiếu thời gian cho quiz — bạn đã skip 2 buổi ôn tập",
        "suggestions": [
            "Giữ pace hiện tại nhưng dành 15 phút cuối mỗi buổi cho quiz",
            "Hoặc giảm tải: bỏ 1 task optional tuần này",
            "Hoặc tăng tốc: học thêm 15 phút/ngày vào cuối tuần",
        ],
    },
}

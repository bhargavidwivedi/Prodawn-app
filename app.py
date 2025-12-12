import random
import streamlit as st
import pandas as pd
import joblib

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(
    page_title="Productivity Predictor",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -----------------------------------------------------------
# CUSTOM CSS (Beige + Light Green Theme + Stylish Heading)
# -----------------------------------------------------------
st.markdown("""
<style>
/* Background */
body, .stApp {
    background-color: #f7f3e9 !important;   /* soft beige */
}

/* Main container */
.block-container {
    padding: 2rem 2rem;
    background-color: #f7f3e9;
}

/* Heading */
h1 {
    font-family: 'Segoe UI', sans-serif;
    font-size: 48px;
    font-weight: bold;
    text-align: center;
    color: #1E3D2D;  /* dark green */
    text-shadow: 2px 2px #B1D9B1;
    margin-bottom: 5px;
}
h2, h3 {
    font-family: 'Segoe UI', sans-serif;
    color: #2e4a35 !important;
}

/* Input labels */
label, .stSelectbox label, .stNumberInput label {
    color: #2e4a35 !important;
    font-weight: 600;
}

/* Buttons */
.stButton>button {
    background-color: #8fbf8f !important;  /* soft green */
    color: #ffffff !important;
    font-size: 18px;
    border-radius: 10px;
    padding: 10px 18px;
    border: none;
}
.stButton>button:hover {
    background-color: #769f76 !important;
}

/* Result card */
.result-card {
    background-color: #F5F5DC; 
    padding: 25px;
    border-radius: 18px;
    border-left: 8px solid #6BAF92;
    margin-top: 25px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.10);
}

/* Dashboard */
.dashboard-box {
    background-color: #E4F5E8; 
    padding: 18px;
    border-radius: 14px;
    margin-top: 20px;
    border-left: 5px solid #8BC6A8;
}

/* Text styles */
.mini-title {
    font-size: 22px;
    color: #40644B;
    font-weight: bold;
}

.predicted-text {
    font-size: 28px;
    font-weight: bold;
    color: #1E3D2D;  /* dark green */
}

.motivation {
    margin-top: 10px;
    font-size: 18px;
    color: #2F4F4F;
    font-style: italic;
}

/* Dashboard metric values */
[data-testid="stMetricValue"] {
    color: #1E3D2D !important;  /* dark green values */
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# MAIN HEADING
# -----------------------------------------------------------
st.markdown("""
<h1>Productivity Predictor</h1>
<p style="text-align:center; font-size:18px; color:#40644B;">
Plan smarter. Work calmer. Achieve more.
</p>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# TRY LOADING MODEL & COLUMNS
# -----------------------------------------------------------
try:
    model = joblib.load("productivity_model.pkl")
    X_columns = joblib.load("columns.pkl")
    model_loaded = True
except:
    model_loaded = False

if not model_loaded:
    st.error("Model files not found! Make sure 'productivity_model.pkl' and 'columns.pkl' are in the same folder.")
    st.stop()

# -----------------------------------------------------------
# USER INPUT SECTION
# -----------------------------------------------------------
st.markdown("### Enter Task Details")
task_duration = st.number_input("Task Duration (minutes):", min_value=1, max_value=300, value=30)
procrastination_choice = st.selectbox("Procrastination Level:", ["Low", "Medium", "High"])
energy_choice = st.selectbox("Energy Level:", ["Low", "Medium", "High"])
mood_choice = st.selectbox("Mood Level:", ["Bad", "Neutral", "Good"])
category_choice = st.selectbox("Task Category:", ["Work", "Study", "Exercise", "Personal"])
day_choice = st.selectbox("Day of the Week:", 
                          ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])

procrastination_map = {"Low": 1, "Medium": 2, "High": 3}
energy_map = {"Low": 1, "Medium": 2, "High": 3}
mood_map = {"Bad": 1, "Neutral": 2, "Good": 3}

# -----------------------------------------------------------
# PREDICT BUTTON
# -----------------------------------------------------------
if st.button("Predict Productivity"):

    input_dict = {
        "task_duration": task_duration,
        "procrastination_time": procrastination_map[procrastination_choice],
        "energy_level": energy_map[energy_choice],
        "mood_level": mood_map[mood_choice],
        "category": category_choice,
        "day_of_week": day_choice
    }

    input_df = pd.DataFrame([input_dict])
    input_df = pd.get_dummies(input_df, columns=["category", "day_of_week"])
    input_df = input_df.reindex(columns=X_columns, fill_value=0)

    prediction = model.predict(input_df)[0]

    # ---------------- RESULT CARD ----------------
    st.markdown("<div class='result-card'>", unsafe_allow_html=True)
    if prediction == 1:
        st.markdown("<div class='predicted-text'>This task is likely to be PRODUCTIVE.</div>", unsafe_allow_html=True)
        productive_quotes = [
            "Great job! This task aligns perfectly with your productive rhythm.",
            "You're in the right mindset — make the most of this energy!",
            "Excellent! Today is the perfect day to accomplish this task.",
            "Your focus is strong. You’re ready to make real progress."
        ]
        st.markdown(f"<div class='motivation'>{random.choice(productive_quotes)}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='predicted-text'>This task may be UNPRODUCTIVE right now.</div>", unsafe_allow_html=True)
        unproductive_quotes = [
            "Don’t worry — productivity isn’t always at 100%. Try a small start!",
            "Maybe break the task into tiny steps to reduce resistance.",
            "A short break or a mindset reset might help you regain momentum.",
            "You’ve got this — try doing just 2 minutes to get started!"
        ]
        st.markdown(f"<div class='motivation'>{random.choice(unproductive_quotes)}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- DASHBOARD PANEL ----------------
    st.markdown("<div class='dashboard-box'>", unsafe_allow_html=True)
    st.markdown("<div class='mini-title'>📊 Task Snapshot</div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Task Duration", f"{task_duration} min")
    with c2:
        st.metric("Energy Level", energy_choice)
    with c3:
        st.metric("Mood Level", mood_choice)
    st.markdown("</div>", unsafe_allow_html=True)

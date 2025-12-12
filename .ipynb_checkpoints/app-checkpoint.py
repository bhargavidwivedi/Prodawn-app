# app.py
import streamlit as st
import pandas as pd
import joblib
import os

st.set_page_config(page_title="Productivity Predictor", layout="centered")

st.title("⚡ Productivity Predictor")
st.markdown("Predict whether a task will be **productive** or **unproductive** using emoji inputs. "
            "This app expects a trained RandomForest model (`productivity_model.pkl`) and "
            "a saved list of training columns (`columns.pkl`).")

# ---------- Helper: load model and columns ----------
@st.cache_resource(show_spinner=False)
def load_model_and_columns(model_path="productivity_model.pkl", columns_path="columns.pkl"):
    model = None
    columns = None
    if os.path.exists(model_path) and os.path.exists(columns_path):
        model = joblib.load(model_path)
        columns = joblib.load(columns_path)
    return model, columns

model, X_columns = load_model_and_columns()

# If model not found, allow user to upload
if model is None:
    st.warning("Model files not found in the working directory.")
    st.info("Upload `productivity_model.pkl` (your trained model) and `columns.pkl` (X.columns saved with joblib).")
    uploaded_model = st.file_uploader("Upload productivity_model.pkl", type=["pkl"])
    uploaded_columns = st.file_uploader("Upload columns.pkl", type=["pkl"])
    if uploaded_model is not None and uploaded_columns is not None:
        try:
            model = joblib.load(uploaded_model)
            X_columns = joblib.load(uploaded_columns)
            st.success("Model and columns loaded successfully!")
        except Exception as e:
            st.error(f"Failed to load uploaded files: {e}")
            st.stop()
    else:
        st.info("If you haven't exported the model yet, run the training notebook snippet below to create the files.")
        st.markdown("""
        **Snippet to save model & columns (run in your training notebook):**
        ```py
        import joblib
        joblib.dump(rf_model, "productivity_model.pkl")
        joblib.dump(X.columns, "columns.pkl")
        ```
        """)
        st.stop()

# ---------- Emoji mappings (convert selection -> numeric) ----------
energy_map = {
    "😴 Very Low": 1,
    "🥱 Low": 3,
    "🙂 Medium": 5,
    "⚡ High": 8,
    "🔥 Very High": 10
}

mood_map = {
    "😢 Bad": 1,
    "😐 Neutral": 3,
    "🙂 Good": 5,
    "😄 Great": 8,
    "🤩 Amazing": 10
}

procrastination_map = {
    "⏳ None": 0,
    "🕒 Little": 5,
    "🕰 Medium": 15,
    "⌛ High": 30
}

categories = ["💼 Work", "📚 Study", "💪 Exercise", "🧘 Relax", "🏠 Household"]
days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

# ---------- Sidebar inputs ----------
st.sidebar.header("Task details")
task_duration = st.sidebar.number_input("Task duration (minutes)", min_value=1, max_value=1440, value=30, step=1)
procrastination_choice = st.sidebar.radio("Procrastination", list(procrastination_map.keys()), index=1)
energy_choice = st.sidebar.radio("Energy level", list(energy_map.keys()), index=2)
mood_choice = st.sidebar.radio("Mood level", list(mood_map.keys()), index=2)
category_choice = st.sidebar.selectbox("Category", categories)
day_choice = st.sidebar.selectbox("Day of week", days)

# ---------- Build input dataframe ----------
if st.button("Predict Productivity"):
    # Prepare numeric features
    input_dict = {
        "task_duration": task_duration,
        "procrastination_time": procrastination_map[procrastination_choice],
        "energy_level": energy_map[energy_choice],
        "mood_level": mood_map[mood_choice],
        # store raw category/day string to be converted to dummies
        "category": category_choice,
        "day_of_week": day_choice
    }

    input_df = pd.DataFrame([input_dict])

    # Convert category/day to match training one-hot encoding
    input_df = pd.get_dummies(input_df, columns=['category', 'day_of_week'])
    # Ensure same columns as training
    input_df = input_df.reindex(columns=X_columns, fill_value=0)

    # Predict
    try:
        pred = model.predict(input_df)[0]
        # If model supports predict_proba, show probability
        prob = None
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(input_df)[0]
            # probability for class 1 (productive)
            prod_prob = prob[1]
        else:
            prod_prob = None

        if pred == 1:
            st.success("🔋 This task is likely to be PRODUCTIVE.")
        else:
            st.info("💤 This task is likely to be UNPRODUCTIVE.")

        if prod_prob is not None:
            st.metric("Predicted probability (productive)", f"{prod_prob:.2f}")

        # Actionable suggestion
        if pred == 1:
            st.write("**Suggestion:** Go ahead and schedule this task now — conditions look good.")
        else:
            st.write("**Suggestion:** Consider reducing distractions, splitting the task, or moving it to a higher-energy time.")

        # Show the processed input for debugging
        with st.expander("Show processed input (one-hot)"):
            st.write(input_df.T)

    except Exception as e:
        st.error(f"Prediction failed: {e}")

# ---------- Footer ----------
st.markdown("---")
st.markdown("Built with ❤️ — you can deploy this to Streamlit Cloud or run locally with `streamlit run app.py`.")

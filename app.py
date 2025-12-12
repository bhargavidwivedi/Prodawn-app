# app.py
# Prodawn - Productivity Predictor (brown-beige theme, single-file with embedded CSS)
# Run: streamlit run app.py

import streamlit as st
from datetime import datetime
import time
import plotly.graph_objects as go

st.set_page_config(page_title="Prodawn — Productivity Predictor", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------
# Embedded CSS (brown / beige theme)
# ---------------------------
CSS = r"""
/* Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;600;700&display=swap');

:root{
  --bg-1: #fbf6f0;       /* cream */
  --bg-2: #f3ebe0;       /* very light beige */
  --panel: #fffaf5;      /* near-white panel */
  --soft-beige: #efe6da; /* beige panels */
  --warm-brown: #8a5a3c; /* primary brown */
  --soft-brown: #b9896a; /* lighter brown */
  --gold: #d9b56a;       /* soft gold */
  --muted: #7b6a5e;      /* muted text */
  --text: #3a2f29;       /* deep text */
  --card-shadow: 0 14px 40px rgba(58,47,41,0.06);
  --radius: 14px;
}

/* Page background and typography */
body, .block-container {
  background: linear-gradient(180deg, var(--bg-1) 0%, var(--bg-2) 65%);
  font-family: "Inter", system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", Arial;
  color: var(--text);
  padding-top: 18px;
}

/* Header / banner */
.header {
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:20px;
  padding:18px 26px;
  margin-bottom:20px;
  border-radius:16px;
  background: linear-gradient(135deg, rgba(138,90,60,0.06), rgba(217,181,106,0.03));
  box-shadow: var(--card-shadow);
  border: 1px solid rgba(138,90,60,0.04);
}
.brand {
  display:flex;
  align-items:center;
  gap:16px;
}
.logo {
  width:72px;
  height:72px;
  border-radius:12px;
  background: linear-gradient(135deg, #b9896a, #8a5a3c);
  display:flex;
  align-items:center;
  justify-content:center;
  color: #fff;
  font-weight:700;
  font-family:"Playfair Display", serif;
  font-size:22px;
  box-shadow: 0 8px 22px rgba(138,90,60,0.12);
  flex-shrink:0;
}
.brand h1 {
  margin:0;
  font-family:"Playfair Display", serif;
  font-size:34px;
  color: var(--text);
  letter-spacing:0.4px;
  line-height:1;
}
.brand p.sub {
  margin:6px 0 0;
  color: var(--muted);
  font-size:13px;
}

/* header right */
.header-actions {
  text-align:right;
  min-width:220px;
}
.header-actions .tag {
  display:inline-block;
  padding:8px 14px;
  border-radius:999px;
  background: linear-gradient(90deg, rgba(217,181,106,0.12), rgba(138,90,60,0.03));
  color: var(--warm-brown);
  font-weight:600;
  font-size:13px;
  box-shadow: 0 6px 18px rgba(138,90,60,0.06);
}

/* layout */
.container {
  display:flex;
  gap:34px;
  align-items:flex-start;
}
.left { flex:2; }
.right { flex:1; min-width:320px; }

/* Section title */
h2.section-title { font-family:"Playfair Display", serif; color:var(--text); margin:8px 0 12px; font-size:20px; }

/* Field label shown above widgets */
.field-label {
  font-size:13px;
  color:var(--muted);
  margin: 8px 0 6px;
  font-weight:600;
  letter-spacing:0.2px;
}

/* Inputs visuals */
input[type="number"], input[type="text"], textarea, select {
  border-radius: 10px;
  padding: 12px 14px;
  border: 1px solid rgba(138,90,60,0.09);
  background: linear-gradient(180deg, var(--panel), rgba(255,255,255,0.96));
  box-shadow: 0 8px 18px rgba(58,47,41,0.03);
  color: var(--text);
  transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
}
input[type="number"]:hover, input[type="text"]:hover, textarea:hover, select:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 30px rgba(58,47,41,0.05);
  border-color: rgba(138,90,60,0.16);
}
input[type="number"]:focus, input[type="text"]:focus, textarea:focus, select:focus {
  outline:none;
  border-color: rgba(217,181,106,0.34);
  box-shadow: 0 22px 38px rgba(217,181,106,0.06);
}

/* Buttons */
.stButton > button {
  background: linear-gradient(180deg, #f7ead0, #e6c689);
  color: var(--text);
  border-radius: 12px;
  padding: 10px 16px;
  font-weight:700;
  box-shadow: 0 12px 30px rgba(138,90,60,0.08);
  border: 1px solid rgba(138,90,60,0.08);
  transition: transform .12s ease, filter .12s ease;
}
.stButton > button:hover {
  transform: translateY(-3px);
  filter: brightness(.96);
}
.stButton > button.secondary {
  background: linear-gradient(180deg, white, #fffaf6);
  color: var(--warm-brown);
  border: 1px solid rgba(138,90,60,0.08);
}

/* Section divider */
.section-divider {
  height:1px;
  margin:18px 0;
  background: linear-gradient(90deg, rgba(138,90,60,0.02), rgba(138,90,60,0.02));
  border-radius:6px;
}

/* Result card base */
.result-card {
  background: var(--panel);
  border-radius: var(--radius);
  padding:16px;
  box-shadow: var(--card-shadow);
  border: 1px solid rgba(58,47,41,0.04);
  transition: transform .16s ease, box-shadow .16s ease, opacity .4s ease;
  opacity: 0;
  transform: translateY(6px);
}
/* show class triggers fade-in */
.result-card.show { opacity: 1; transform: translateY(0); }

/* color variants */
.result-good { background: linear-gradient(180deg, rgba(217,181,106,0.02), rgba(241,238,232,0.9)); border-left: 6px solid #b9896a; }
.result-ok   { background: linear-gradient(180deg, rgba(255,225,180,0.02), rgba(250,247,242,0.95)); border-left: 6px solid #d9b56a; }
.result-bad  { background: linear-gradient(180deg, rgba(255,220,210,0.02), rgba(252,244,242,0.95)); border-left: 6px solid #e5a07a; }

/* progress bar */
.progress-wrap { height:12px; background: rgba(58,47,41,0.03); border-radius:10px; overflow:hidden; margin:12px 0; }
.progress-bar { height:12px; width:0%; border-radius:10px; transition: width .9s cubic-bezier(.2,.8,.2,1); }

/* report card (metrics + chart) */
.report-card {
  display:flex;
  gap:18px;
  align-items:center;
  padding:14px;
  border-radius:12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,246,240,0.95));
  box-shadow: 0 12px 30px rgba(58,47,41,0.04);
  border: 1px solid rgba(58,47,41,0.04);
}

/* snapshot mini-cards */
.snapshot { display:flex; gap:12px; margin-top:12px; }
.card-mini {
  flex:1;
  padding:12px;
  border-radius:12px;
  background: linear-gradient(180deg, var(--soft-beige), rgba(255,255,255,0.95));
  box-shadow: 0 8px 22px rgba(58,47,41,0.03);
  border: 1px solid rgba(58,47,41,0.04);
}
.card-mini .k { font-size:13px; color:var(--muted); }
.card-mini .v { font-size:18px; font-weight:700; color:var(--text); margin-top:6px; }

/* icon box */
.icon {
  width:44px; height:44px; display:inline-flex; align-items:center; justify-content:center;
  border-radius:10px; margin-right:12px; background: linear-gradient(90deg,#fff,#fff7f1);
  color: var(--warm-brown);
  font-weight:700;
}

/* small fade-in animation for cards */
@keyframes fadeInUp {
  from { opacity:0; transform: translateY(8px); }
  to   { opacity:1; transform: translateY(0); }
}
.result-card.show, .card-mini { animation: fadeInUp .45s ease both; }

/* Responsive */
@media (max-width: 980px) {
  .container { flex-direction:column; }
  .header { padding:16px; }
  .brand h1 { font-size:28px; }
}
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ---------------------------
# Helper: compute productivity score (replaceable by your model)
# ---------------------------
def compute_score(duration, procrastination, energy, mood, category):
    # baseline
    score = 55
    # duration influence
    if duration <= 15:
        score += 14
    elif duration <= 30:
        score += 10
    elif duration <= 60:
        score += 4
    elif duration <= 120:
        score -= 4
    else:
        score -= 12

    # procrastination effect
    if procrastination == "Low":
        score += 16
    elif procrastination == "High":
        score -= 18

    # energy & mood
    if energy == "High":
        score += 12
    elif energy == "Low":
        score -= 10

    if mood == "Good":
        score += 8
    elif mood == "Bad":
        score -= 6

    # category small tweak (creative tasks sometimes vary)
    if category == "Creative" and mood == "Good":
        score += 4

    # clamp
    return max(0, min(100, int(score)))

# ---------------------------
# Header HTML
# ---------------------------
header_html = """
<div class="header" role="banner" aria-label="Prodawn header">
  <div class="brand">
    <div class="logo" aria-hidden="true">
      <svg width="44" height="44" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <defs>
          <linearGradient id="g1" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0" stop-color="#b9896a"/>
            <stop offset="1" stop-color="#8a5a3c"/>
          </linearGradient>
        </defs>
        <rect width="64" height="64" rx="12" fill="url(#g1)"/>
        <text x="32" y="38" text-anchor="middle" font-family="Playfair Display, serif" font-size="28" fill="rgba(255,255,255,0.98)" font-weight="700">Pd</text>
      </svg>
    </div>
    <div>
      <h1>Prodawn</h1>
      <p class="sub">Plan smarter, work calmer, achieve more</p>
    </div>
  </div>
  <div class="header-actions" aria-hidden="false">
    <div style="font-size:13px;color:var(--muted); margin-bottom:8px;">Gentle predictions & focused nudges</div>
    <div class="tag">brown-beige aesthetic ✨</div>
  </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ---------------------------
# Main layout: left inputs, right report/snapshot
# ---------------------------
left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown('<h2 class="section-title">Enter Task Details</h2>', unsafe_allow_html=True)
    with st.form(key="task_form"):
        # explicit labels above widgets so headings are always visible
        st.markdown('<div class="field-label">⏱️ Task Duration (minutes)</div>', unsafe_allow_html=True)
        duration = st.number_input('', min_value=1, max_value=24*60, value=60, step=5, key="duration")

        st.markdown('<div class="field-label">🕰️ Procrastination Level</div>', unsafe_allow_html=True)
        procrastination = st.selectbox('', ["Low", "Medium", "High"], index=1, key="procrastination")

        st.markdown('<div class="field-label">⚡ Energy Level</div>', unsafe_allow_html=True)
        energy = st.selectbox('', ["Low", "Medium", "High"], index=1, key="energy")

        st.markdown('<div class="field-label">😊 Mood Level</div>', unsafe_allow_html=True)
        mood = st.selectbox('', ["Bad", "Okay", "Good"], index=2, key="mood")

        st.markdown('<div class="field-label">🏷️ Task Category</div>', unsafe_allow_html=True)
        category = st.selectbox('', ["Work", "Study", "Personal", "Errand", "Creative"], index=0, key="category")

        st.markdown('<div class="field-label">📅 Day of the Week</div>', unsafe_allow_html=True)
        day = st.selectbox('', ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"], index=datetime.now().weekday(), key="day")

        st.markdown('<div class="field-label">✍️ Quick note (optional)</div>', unsafe_allow_html=True)
        note = st.text_input('', placeholder="One-sentence goal or subtask", key="note")

        submitted = st.form_submit_button("Predict Productivity")

with right_col:
    st.markdown('<h2 class="section-title">Snapshot & Tip</h2>', unsafe_allow_html=True)
    initial_card = """
    <div class="result-card" role="region" aria-live="polite">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:13px; color:var(--muted)">Prediction</div>
          <div style="font-weight:700; font-size:18px; color:var(--text); margin-top:6px;">Ready when you are</div>
        </div>
        <div class="badge ok" style="background:linear-gradient(90deg,#d9b56a,#b9896a); color:#3a2f29;">Let's begin</div>
      </div>
      <div class="section-divider"></div>
      <div style="color:var(--muted); font-size:13px;">Fill the form and press Predict to see a friendly suggestion and report card.</div>
    </div>
    """
    st.markdown(initial_card, unsafe_allow_html=True)

# ---------------------------
# When submitted: compute score and render report
# ---------------------------
if submitted:
    # small spinner for pleasant feel
    with st.spinner("Generating report..."):
        time.sleep(0.8)

    score = compute_score(duration, procrastination, energy, mood, category)
    prog_width = f"{score}%"

    # choose tone and visuals
    if score >= 80:
        tone_class = "result-good"
        badge_html = '<span class="badge good">Highly productive ✓</span>'
        title = "You're in a great spot — high productivity ahead!"
        tip = "Keep momentum: start a focused interval and build on it."
        bar_style = "background: linear-gradient(90deg,#b9896a,#8a5a3c);"
        motivation = "Excellent — your chances of completing this task efficiently are high. Celebrate a small win and go for a focused block!"
    elif score >= 50:
        tone_class = "result-ok"
        badge_html = '<span class="badge ok">Moderately productive</span>'
        title = "Good — a few adjustments could help."
        tip = "Try a 10-minute warm-up, remove a single distraction, or divide the task."
        bar_style = "background: linear-gradient(90deg,#d9b56a,#b9896a);"
        motivation = "Nice — you're close. Small actions like a short timer or a simpler first step will help."
    else:
        tone_class = "result-bad"
        badge_html = '<span class="badge bad">Needs a nudge</span>'
        title = "This might be a hard window for productivity."
        tip = "Start with 2 minutes or pick a tiny doable step to reduce friction."
        bar_style = "background: linear-gradient(90deg,#e5a07a,#d98968);"
        motivation = "That's okay — begin with tiny progress. Even 2 minutes can create momentum."

    # Result summary card
    result_html = f"""
    <div class="result-card show {tone_class}" role="region" aria-live="polite">
      <div style="display:flex; justify-content:space-between; align-items:flex-start; gap:12px;">
        <div style="flex:1;">
          <div style="font-size:13px; color:var(--muted);">Prediction • confidence {score}%</div>
          <div style="font-weight:700; font-size:18px; color:var(--text); margin-top:6px;">{title}</div>
          <div style="color:var(--muted); font-size:14px; margin-top:8px;">{tip}</div>
        </div>
        <div style="min-width:150px; display:flex; align-items:center; justify-content:flex-end;">
          {badge_html}
        </div>
      </div>

      <div class="section-divider"></div>

      <div class="progress-wrap" aria-hidden="true">
        <div class="progress-bar" style="width:{prog_width}; {bar_style}"></div>
      </div>

      <div style="margin-top:10px; color:var(--muted); font-size:14px;">{motivation}</div>
    </div>
    """
    st.markdown(result_html, unsafe_allow_html=True)

    # Report card area (chart + details)
    # Plotly gauge (circular) to visualize productivity percentage
    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={'suffix':'%', 'font': {'size':20, 'color': '#3a2f29'}},
        gauge={
            'axis': {'range':[0,100], 'tickcolor': '#7b6a5e'},
            'bar': {'color': '#b9896a', 'thickness':0.28},
            'bgcolor': "rgba(0,0,0,0)",
            'steps': [
                {'range':[0,49], 'color':'rgba(234,140,95,0.15)'},
                {'range':[50,79], 'color':'rgba(217,181,106,0.12)'},
                {'range':[80,100], 'color':'rgba(185,137,106,0.12)'}
            ],
            'threshold': {
                'line': {'color': "#8a5a3c", 'width': 3},
                'thickness': 0.75,
                'value': score
            }
        }
    ))
    gauge.update_layout(margin=dict(l=20,r=20,t=20,b=20), paper_bgcolor="rgba(0,0,0,0)", height=260)

    # mini bar chart showing components (simple visualization)
    comp_names = ['Duration','Procrastination','Energy','Mood']
    # approximate contributions for display
    # Convert qualitative -> numeric for visualization purpose
    p_map = {'Low':80, 'Medium':50, 'High':20}
    e_map = {'Low':20, 'Medium':50, 'High':80}
    m_map = {'Bad':20, 'Okay':50, 'Good':80}
    components = [
        max(0, min(100, int(100 - (duration / max(duration,60))*20))),  # shorter gets higher
        p_map.get(procrastination,50),
        e_map.get(energy,50),
        m_map.get(mood,50)
    ]
    bar = go.Figure(go.Bar(
        x=components,
        y=comp_names,
        orientation='h',
        marker=dict(color=['#b9896a','#d9b56a','#b9896a','#b9896a']),
        text=[f"{c}%" for c in components],
        textposition='inside',
        insidetextanchor='middle'
    ))
    bar.update_layout(margin=dict(l=10,r=10,t=10,b=10), height=240, xaxis=dict(range=[0,100], visible=False), paper_bgcolor="rgba(0,0,0,0)")

    # Render report card: plot + key stats
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    col_gauge, col_stats = st.columns([1,1], gap="small")
    with col_gauge:
        st.plotly_chart(gauge, use_container_width=True, config={'displayModeBar': False})
    with col_stats:
        st.plotly_chart(bar, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # Snapshot mini-cards using Streamlit columns (explicit labels shown)
    st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1,1,1,1], gap="small")
    with c1:
        st.markdown(
            f"""
            <div class="card-mini">
              <div style="display:flex; align-items:center;">
                <div class="icon">⏱️</div>
                <div>
                  <div class="k">Duration</div>
                  <div class="v">{duration} min</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f"""
            <div class="card-mini">
              <div style="display:flex; align-items:center;">
                <div class="icon">🕰️</div>
                <div>
                  <div class="k">Procrastination</div>
                  <div class="v">{procrastination}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True
        )
    with c3:
        st.markdown(
            f"""
            <div class="card-mini">
              <div style="display:flex; align-items:center;">
                <div class="icon">⚡</div>
                <div>
                  <div class="k">Energy</div>
                  <div class="v">{energy}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True
        )
    with c4:
        st.markdown(
            f"""
            <div class="card-mini">
              <div style="display:flex; align-items:center;">
                <div class="icon">😊</div>
                <div>
                  <div class="k">Mood</div>
                  <div class="v">{mood}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True
        )

    # small suggestions area
    st.markdown(
        f"""
        <div style="margin-top:12px; display:flex; gap:12px; align-items:flex-start;">
          <div style="flex:1;">
            <div style="font-weight:700; color:var(--text); margin-bottom:6px;">Suggested micro-actions</div>
            <ul style="color:var(--muted); margin-top:0;">
              <li>{ "Great work — set a 25-minute focus block and keep the momentum." if score>=80 else ("Try a 10-minute warm-up and remove one distraction." if score>=50 else "Begin with a 2-minute tiny action — small wins reduce friction.") }</li>
              <li>Set a timer and remove one major distraction (phone / unnecessary tab).</li>
              <li>Break the task into a 2-minute starter and a follow-up chunk.</li>
            </ul>
          </div>
          <div style="min-width:160px;">
            <div class="stButton"><button class="secondary" onclick="void(0)">Save report</button></div>
            <div style="height:8px"></div>
            <div style="font-size:13px;color:var(--muted);margin-top:8px;">Category: <strong style="color:var(--text)">{category}</strong><br/>Day: <strong style="color:var(--text)">{day}</strong></div>
          </div>
        </div>
        """, unsafe_allow_html=True
    )

    # small celebration / visual if very high
    if score >= 92:
        st.balloons()

# Footer
st.markdown(
    """
    <div style="margin-top:26px; color:var(--muted); font-size:13px;">
      Built with care — Prodawn helps you turn intentions into gentle momentum.
    </div>
    """,
    unsafe_allow_html=True,
)
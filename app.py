
# app.py
# Prodawn - Productivity Predictor (brown-beige theme) - light pastel colors (no dark colors)
# Run: streamlit run app.py
#
# This single-file app uses matplotlib (no Plotly). Colors chosen to be soft / non-dark.

import streamlit as st
from datetime import datetime
import time
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Prodawn — Productivity Predictor", layout="wide", initial_sidebar_state="collapsed")

# ---------------------------
# Color configuration -- soft, non-dark pastel colors
# ---------------------------
# Light/soft palette (no dark colors)
GOOD_COLOR = "#F6E9B8"    # productive (very light gold)
OK_COLOR   = "#FBEDD3"    # moderate (soft warm amber)
BAD_COLOR  = "#FDE7E0"    # unproductive (pale peach)

# Slightly richer (but still soft) variants for chart accents
GOOD_COLOR_ACCENT = "#F0DC9A"
OK_COLOR_ACCENT = "#F7DFC0"
BAD_COLOR_ACCENT = "#F7CBC0"

# ---------------------------
# Embedded CSS (brown / beige theme, light tones)
# ---------------------------
CSS = r"""
/* Fonts */
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;600;700&display=swap');

:root{
  --bg-1: #fcf8f4;       /* cream */
  --bg-2: #f8efe3;       /* light beige */
  --panel: #fffaf6;      /* near-white panel */
  --soft-beige: #f3e9dd; /* soft beige panels */
  --warm-brown: #b9937b; /* warm brown (soft) */
  --muted: #7f6f66;      /* muted text */
  --text: #4e3f36;       /* still soft, not dark */
  --card-shadow: 0 12px 28px rgba(78,63,54,0.06);
  --radius: 12px;
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
  gap:18px;
  padding:18px 22px;
  margin-bottom:18px;
  border-radius:14px;
  background: linear-gradient(135deg, rgba(185,147,119,0.06), rgba(247,227,187,0.03));
  box-shadow: var(--card-shadow);
  border: 1px solid rgba(185,147,119,0.04);
}
.brand {
  display:flex;
  align-items:center;
  gap:14px;
}
.logo {
  width:68px;
  height:68px;
  border-radius:12px;
  background: linear-gradient(135deg, #d9b78f, #c9a97a);
  display:flex;
  align-items:center;
  justify-content:center;
  color: #fff;
  font-weight:700;
  font-family:"Playfair Display", serif;
  font-size:22px;
  box-shadow: 0 8px 20px rgba(185,147,119,0.10);
  flex-shrink:0;
}
.brand h1 {
  margin:0;
  font-family:"Playfair Display", serif;
  font-size:32px;
  color: var(--text);
  letter-spacing:0.3px;
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
  min-width:200px;
}
.header-actions .tag {
  display:inline-block;
  padding:8px 12px;
  border-radius:999px;
  background: linear-gradient(90deg, rgba(217,181,106,0.10), rgba(185,147,119,0.02));
  color: var(--warm-brown);
  font-weight:600;
  font-size:13px;
  box-shadow: 0 6px 14px rgba(185,147,119,0.06);
}

/* layout */
.container {
  display:flex;
  gap:28px;
  align-items:flex-start;
}
.left { flex:2; }
.right { flex:1; min-width:300px; }

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
  border: 1px solid rgba(185,147,119,0.10);
  background: linear-gradient(180deg, var(--panel), rgba(255,255,255,0.98));
  box-shadow: 0 8px 16px rgba(78,63,54,0.03);
  color: var(--text);
  transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
}
input[type="number"]:hover, input[type="text"]:hover, textarea:hover, select:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 26px rgba(78,63,54,0.04);
  border-color: rgba(185,147,119,0.16);
}
input[type="number"]:focus, input[type="text"]:focus, textarea:focus, select:focus {
  outline:none;
  border-color: rgba(217,181,106,0.28);
  box-shadow: 0 20px 36px rgba(217,181,106,0.05);
}

/* Buttons */
.stButton > button {
  background: linear-gradient(180deg, #fbf1d8, #f1dbab);
  color: var(--text);
  border-radius: 12px;
  padding: 10px 16px;
  font-weight:700;
  box-shadow: 0 10px 28px rgba(185,147,119,0.08);
  border: 1px solid rgba(185,147,119,0.08);
  transition: transform .12s ease, filter .12s ease;
}
.stButton > button:hover {
  transform: translateY(-3px);
  filter: brightness(.98);
}

/* make form submit button more prominent */
.stForm .stButton > button {
  width: 100%;
  padding: 14px 18px;
  font-size: 16px;
  border-radius: 12px;
  box-shadow: 0 14px 34px rgba(185,147,119,0.10);
  background: linear-gradient(180deg, #fff3d9, #f3d59a);
}

/* Section divider */
.section-divider {
  height:1px;
  margin:14px 0;
  background: linear-gradient(90deg, rgba(185,147,119,0.02), rgba(185,147,119,0.02));
  border-radius:6px;
}

/* Result card */
.result-card {
  background: var(--panel);
  border-radius: 12px;
  padding:14px;
  box-shadow: var(--card-shadow);
  border: 1px solid rgba(78,63,54,0.04);
  transition: transform .14s ease, box-shadow .14s ease, opacity .4s ease;
  opacity: 0;
  transform: translateY(6px);
}
.result-card.show {
  opacity: 1;
  transform: translateY(0);
}

/* color variants (soft) */
.result-good { background: linear-gradient(180deg, rgba(246,233,184,0.5), rgba(255,255,255,0.95)); border-left: 6px solid rgba(185,147,119,0.20); }
.result-ok   { background: linear-gradient(180deg, rgba(251,237,211,0.5), rgba(255,255,255,0.95)); border-left: 6px solid rgba(217,181,106,0.18); }
.result-bad  { background: linear-gradient(180deg, rgba(253,231,225,0.5), rgba(255,255,255,0.95)); border-left: 6px solid rgba(229,160,122,0.18); }

/* progress */
.progress-wrap { height:12px; background: rgba(78,63,54,0.03); border-radius:10px; overflow:hidden; margin:12px 0; }
.progress-bar { height:12px; width:0%; border-radius:10px; transition: width .9s cubic-bezier(.2,.8,.2,1); }

/* report card (metrics + chart) */
.report-card {
  display:flex;
  gap:14px;
  align-items:center;
  padding:12px;
  border-radius:12px;
  background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(250,246,240,0.95));
  box-shadow: 0 12px 26px rgba(78,63,54,0.04);
  border: 1px solid rgba(78,63,54,0.04);
}

/* snapshot mini-cards */
.snapshot { display:flex; gap:12px; margin-top:12px; }
.card-mini {
  flex:1;
  padding:12px;
  border-radius:12px;
  background: linear-gradient(180deg, var(--soft-beige), rgba(255,255,255,0.95));
  box-shadow: 0 8px 18px rgba(78,63,54,0.03);
  border: 1px solid rgba(78,63,54,0.04);
}
.card-mini .k { font-size:13px; color:var(--muted); }
.card-mini .v { font-size:16px; font-weight:700; color:var(--text); margin-top:6px; }

/* icon box */
.icon {
  width:40px; height:40px; display:inline-flex; align-items:center; justify-content:center;
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
  .header { padding:14px; }
  .brand h1 { font-size:28px; }
}
"""
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

# ---------------------------
# Helper: compute productivity score (simple heuristic)
# ---------------------------
def compute_score(duration, procrastination, energy, mood, category):
    score = 55
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
    if procrastination == "Low":
        score += 16
    elif procrastination == "High":
        score -= 18
    if energy == "High":
        score += 12
    elif energy == "Low":
        score -= 10
    if mood == "Good":
        score += 8
    elif mood == "Bad":
        score -= 6
    if category == "Creative" and mood == "Good":
        score += 4
    return max(0, min(100, int(score)))

# ---------------------------
# Header HTML
# ---------------------------
header_html = f"""
<div class="header" role="banner" aria-label="Prodawn header">
  <div class="brand">
    <div class="logo" aria-hidden="true">
      <svg width="44" height="44" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
        <defs>
          <linearGradient id="g1" x1="0" x2="1" y1="0" y2="1">
            <stop offset="0" stop-color="#d9b78f"/>
            <stop offset="1" stop-color="#c9a97a"/>
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
    <div class="tag">soft brown-beige palette ✨</div>
  </div>
</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# ---------------------------
# Main layout: left inputs, right snapshot/report
# ---------------------------
left_col, right_col = st.columns([2, 1], gap="large")

with left_col:
    st.markdown('<h2 class="section-title">Enter Task Details</h2>', unsafe_allow_html=True)
    with st.form(key="task_form"):
        # Visible labels above widgets
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

        # Prominent final button (text changed earlier as requested)
        submitted = st.form_submit_button("Predict Productivity ✨")

with right_col:
    st.markdown('<h2 class="section-title">Snapshot & Tip</h2>', unsafe_allow_html=True)
    initial_card = f"""
    <div class="result-card" role="region" aria-live="polite">
      <div style="display:flex; justify-content:space-between; align-items:center;">
        <div>
          <div style="font-size:13px; color:var(--muted)">Prediction</div>
          <div style="font-weight:700; font-size:18px; color:var(--text); margin-top:6px;">Ready when you are</div>
        </div>
        <div style="padding:8px 12px; border-radius:999px; background:linear-gradient(90deg,{OK_COLOR},{OK_COLOR_ACCENT}); color:#3a2f29; font-weight:700;">Let's begin</div>
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
    with st.spinner("Generating report..."):
        time.sleep(0.7)

    score = compute_score(duration, procrastination, energy, mood, category)
    prog_width = f"{score}%"

    # choose tone and visuals with soft pastel colors
    if score >= 80:
        tone_class = "result-good"
        badge_html = f'<span style="display:inline-block;padding:8px 12px;border-radius:999px;background:{GOOD_COLOR};color:#4e3f36;font-weight:700;">Highly productive ✓</span>'
        title = "You're in a great spot — high productivity ahead!"
        tip = "Keep momentum: start a focused interval and build on it."
        bar_color = GOOD_COLOR_ACCENT
        motivation = "Excellent — your chances of completing this task efficiently are high. Celebrate a small win and go for a focused block!"
    elif score >= 50:
        tone_class = "result-ok"
        badge_html = f'<span style="display:inline-block;padding:8px 12px;border-radius:999px;background:{OK_COLOR};color:#4e3f36;font-weight:700;">Moderately productive</span>'
        title = "Good — a few adjustments could help."
        tip = "Try a 10-minute warm-up, remove a single distraction, or divide the task."
        bar_color = OK_COLOR_ACCENT
        motivation = "Nice — you're close. Small actions like a short timer or a simpler first step will help."
    else:
        tone_class = "result-bad"
        badge_html = f'<span style="display:inline-block;padding:8px 12px;border-radius:999px;background:{BAD_COLOR};color:#4e3f36;font-weight:700;">Needs a nudge</span>'
        title = "This might be a hard window for productivity."
        tip = "Start with 2 minutes or pick a tiny doable step to reduce friction."
        bar_color = BAD_COLOR_ACCENT
        motivation = "That's okay — begin with tiny progress. Even 2 minutes can create momentum."

    # Result summary card (soft colors, no dark contrasts)
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
        <div class="progress-bar" style="width:{prog_width}; background: linear-gradient(90deg,{bar_color},{bar_color});"></div>
      </div>

      <div style="margin-top:10px; color:var(--muted); font-size:14px;">{motivation}</div>
    </div>
    """
    st.markdown(result_html, unsafe_allow_html=True)

    # Report area: donut chart (matplotlib) + horizontal component bars
    st.markdown('<div style="height:12px"></div>', unsafe_allow_html=True)
    st.markdown('<div class="report-card">', unsafe_allow_html=True)
    col_chart, col_stats = st.columns([1,1], gap="small")

    # Prepare component approximations
    p_map = {'Low':80, 'Medium':50, 'High':20}
    e_map = {'Low':20, 'Medium':50, 'High':80}
    m_map = {'Bad':20, 'Okay':50, 'Good':80}
    components = [
        max(0, min(100, int(100 - (duration / max(duration,60)) * 20))),  # shorter -> higher
        p_map.get(procrastination, 50),
        e_map.get(energy, 50),
        m_map.get(mood, 50)
    ]
    comp_names = ['Duration', 'Procrastination', 'Energy', 'Mood']
    comp_colors = [GOOD_COLOR, OK_COLOR, GOOD_COLOR, GOOD_COLOR]

    # Donut chart (productivity percentage)
    with col_chart:
        fig1, ax1 = plt.subplots(figsize=(3.0, 3.0), dpi=100)
        size = score
        remaining = 100 - score
        wedges, texts = ax1.pie([size, remaining],
                                colors=[bar_color, '#f6efe6'],
                                startangle=90, counterclock=False,
                                wedgeprops=dict(width=0.36, edgecolor='white'))
        centre_circle = plt.Circle((0, 0), 0.60, color='white')
        ax1.add_artist(centre_circle)
        ax1.set(aspect="equal")
        ax1.text(0, 0.03, f"{score}%", horizontalalignment='center', verticalalignment='center',
                 fontsize=20, fontweight='700', color='#4e3f36')
        ax1.text(0, -0.2, "Productivity", horizontalalignment='center', verticalalignment='center',
                 fontsize=10, color='#7f6f66')
        plt.tight_layout()
        st.pyplot(fig1)
        plt.close(fig1)

    # Horizontal bars showing component approximations
    with col_stats:
        fig2, ax2 = plt.subplots(figsize=(4, 3.0), dpi=100)
        y_pos = list(range(len(comp_names)))
        ax2.barh(y_pos, components, color=comp_colors, edgecolor='white')
        ax2.set_yticks(y_pos)
        ax2.set_yticklabels(comp_names)
        ax2.set_xlim(0, 100)
        ax2.invert_yaxis()
        for i, v in enumerate(components):
            # place percentage inside or beside bar depending on width
            if v > 18:
                ax2.text(v - 6, i, f"{v}%", va='center', ha='right', color='white', fontsize=9, fontweight='700')
            else:
                ax2.text(v + 2, i, f"{v}%", va='center', ha='left', color='#4e3f36', fontsize=9, fontweight='700')
        ax2.xaxis.set_visible(False)
        plt.box(False)
        plt.tight_layout()
        st.pyplot(fig2)
        plt.close(fig2)

    st.markdown('</div>', unsafe_allow_html=True)

    # Snapshot mini-cards using Streamlit columns
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

    # Suggestions & CTA
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

    # light celebration for very high score
    if score >= 95:
        st.balloons()

# Footer
st.markdown(
    """
    <div style="margin-top:22px; color:var(--muted); font-size:13px;">
      Built with care — Prodawn helps you turn intentions into gentle momentum.
    </div>
    """,
    unsafe_allow_html=True,
)
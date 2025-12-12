# Quick example: render those two card-mini blocks correctly in Streamlit.
# Save & run: streamlit run render_cards.py

import streamlit as st

st.set_page_config(page_title="Card mini render demo", layout="centered")

# Inject minimal CSS required for .card-mini, .icon, .k, .v
CSS = """
<style>
.card-mini{
  flex:1; padding:12px; border-radius:12px; background: linear-gradient(180deg, rgba(255,255,255,0.98), rgba(240,247,243,0.8));
  box-shadow: 0 6px 18px rgba(34,65,52,0.03); border: 1px solid rgba(36,65,52,0.04);
  text-align:left; display:inline-block; vertical-align:top; margin-right:10px;
}
.icon { width:34px; height:34px; display:inline-flex; align-items:center; justify-content:center;
  border-radius:10px; margin-right:10px; background:linear-gradient(90deg,#fff,#f6f6f6);
}
.k { font-size:13px; color:#6b786a; }
.v { font-size:18px; font-weight:700; color:#244136; margin-top:6px; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# Important: DO NOT wrap your HTML inside triple backticks or use st.code/st.write for this block.
# Use st.markdown(..., unsafe_allow_html=True) so Streamlit will render the HTML markup.

html = """
<div style="display:flex; gap:12px; align-items:flex-start;">
  <div class="card-mini">
    <div style="display:flex; align-items:center;">
      <div class="icon">
        <svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none'>
          <path d='M12 3v3' stroke='#f6a65a' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'/>
          <path d='M12 18v3' stroke='#8ed1b9' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'/>
          <path d='M4 12h3' stroke='#bfe8d9' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'/>
          <path d='M17 12h3' stroke='#5aa882' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'/>
        </svg>
      </div>
      <div>
        <div class="k">Energy</div>
        <div class="v">Medium</div>
      </div>
    </div>
  </div>

  <div class="card-mini">
    <div style="display:flex; align-items:center;">
      <div class="icon">
        <svg xmlns='http://www.w3.org/2000/svg' width='18' height='18' viewBox='0 0 24 24' fill='none'>
          <path d='M12 3c2 0 3 2 3 4s-1 4-3 4-3-2-3-4 1-4 3-4z' stroke='#5aa882' stroke-width='1.4' stroke-linecap='round' stroke-linejoin='round'/>
          <path d='M21 21c-.8-3.6-3.8-6-9-6s-8.2 2.4-9 6' stroke='#bfe8d9' stroke-width='1.4' stroke-linecap='round' stroke-linejoin='round'/>
        </svg>
      </div>
      <div>
        <div class="k">Mood</div>
        <div class="v">Good</div>
      </div>
    </div>
  </div>
</div>
"""

st.markdown(html, unsafe_allow_html=True)
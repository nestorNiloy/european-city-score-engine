import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
sys.path.insert(0, '/content/city_score_engine')

from data.fetcher import fetch_all_cities
from data.scorer import compute_scores

st.set_page_config(page_title="European City Score Engine", page_icon="🏙️", layout="wide")

st.title("🏙️ European City Score Engine")
st.markdown("Compare top European tech cities based on what matters most to you.")

# --- Sidebar ---
st.sidebar.header("⚖️ Adjust Your Priorities")
st.sidebar.markdown("Set how much each factor matters. Total must equal 100.")

w_jobs     = st.sidebar.slider("💼 Job Market",        0, 100, 35, 5)
w_cost     = st.sidebar.slider("💰 Cost of Living",    0, 100, 30, 5)
w_safety   = st.sidebar.slider("🛡️ Safety",            0, 100, 20, 5)
w_internet = st.sidebar.slider("🌐 Internet Speed",    0, 100, 15, 5)

total = w_jobs + w_cost + w_safety + w_internet

if total != 100:
    st.sidebar.error(f"⚠️ Weights sum to {total}. Please adjust to exactly 100.")
    st.stop()
else:
    st.sidebar.success("✅ Weights sum to 100")

# --- Fetch & Score ---
with st.spinner("Fetching live job data from Adzuna..."):
    df = fetch_all_cities()

scored_df = compute_scores(df, w_jobs, w_cost, w_safety, w_internet)

# --- Top City Banner ---
top_city = scored_df.iloc[0]["City"]
top_score = scored_df.iloc[0]["Final Score"]
st.markdown(f"## 🥇 Best City for You: **{top_city}** (Score: {top_score})")
st.divider()

# --- Rankings Table ---
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📊 City Rankings")
    display_df = scored_df[["City", "Job Score", "Cost Score", "Safety Score", "Internet Score", "Final Score"]].copy()
    display_df.index = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    st.dataframe(display_df.style.format("{:.1f}", subset=["Job Score", "Cost Score", "Safety Score", "Internet Score", "Final Score"]), use_container_width=True)

with col2:
    st.subheader("🏆 Final Score Comparison")
    fig_bar = px.bar(
        scored_df,
        x="City",
        y="Final Score",
        color="Final Score",
        color_continuous_scale="teal",
        text="Final Score",
        range_y=[0, 100]
    )
    fig_bar.update_traces(texttemplate='%{text:.1f}', textposition='outside')
    fig_bar.update_layout(showlegend=False, coloraxis_showscale=False, plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_bar, use_container_width=True)

# --- Radar Chart ---
st.subheader("🕸️ Factor Breakdown by City")
categories = ["Job Score", "Cost Score", "Safety Score", "Internet Score"]
fig_radar = go.Figure()
colors = ["#00b4d8", "#f77f00", "#06d6a0", "#e63946", "#8338ec"]

for i, row in scored_df.iterrows():
    values = [row[c] for c in categories] + [row[categories[0]]]
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        name=row["City"],
        line_color=colors[i - 1]
    ))

fig_radar.update_layout(
    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
    showlegend=True,
    height=500
)
st.plotly_chart(fig_radar, use_container_width=True)

# --- Raw Data ---
with st.expander("📋 View Raw Data"):
    st.dataframe(df, use_container_width=True)

st.caption("Data sources: Adzuna API (live job counts) · Numbeo 2024 (cost of living, safety) · Ookla Speedtest 2024 (internet speed)")

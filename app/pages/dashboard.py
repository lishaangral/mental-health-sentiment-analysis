import streamlit as st
import pandas as pd
import json
import os
import altair as alt
from datetime import datetime

st.set_page_config(page_title="Mental Health Dashboard", layout="wide")
st.title("📊 Mental Health Sentiment Monitoring Dashboard")

log_file = "data/prediction_log.jsonl"

# Helper to parse and structure data
def load_logs(log_file):
    with open(log_file) as f:
        logs = [json.loads(line) for line in f]

    for log in logs:
        log['timestamp'] = pd.to_datetime(log['timestamp'])
        result = log.get("result", {})
        if isinstance(result, list):
            for entry in result:
                log[entry['label']] = entry['score']
        elif isinstance(result, dict):
            log[result['label']] = result['score']
    return pd.DataFrame(logs)

if os.path.exists(log_file):
    df = load_logs(log_file)

    st.sidebar.header("📌 Preferences")
    show_raw_data = st.sidebar.checkbox("Show Raw Logs Table", value=False)

    st.subheader("🔍 Sentiment Score Trends")
    
    melt_cols = [col for col in df.columns if col not in ['timestamp', 'window', 'text', 'result']]
    df_melted = df.melt(id_vars='timestamp', value_vars=melt_cols, var_name='Label', value_name='Score')

    line_chart = alt.Chart(df_melted).mark_line(point=True).encode(
        x='timestamp:T',
        y='Score:Q',
        color='Label:N',
        tooltip=['timestamp:T', 'Label:N', 'Score:Q']
    ).interactive().properties(width=1000, height=400)

    st.altair_chart(line_chart, use_container_width=True)

    st.subheader("📌 Metrics Overview")
    metrics = df_melted.groupby("Label")['Score'].agg(['mean', 'max']).reset_index()
    metrics.columns = ['Label', 'Average Score', 'Max Score']
    st.dataframe(metrics.style.format("{:.2f}"))

    st.subheader("📒 Key Insights")
    insights = []
    if any((df[label] > 0.8).sum() > 2 for label in melt_cols if "negative" in label.lower()):
        insights.append("🚨 **Frequent high-negative sentiment detected. Consider taking breaks or exploring calming exercises.**")
    if any((df[label] > 0.85).sum() > 3 for label in melt_cols if "positive" in label.lower() or "happy" in label.lower()):
        insights.append("😊 **You’ve shown strong positive sentiment recently. Great job maintaining balance!**")
    if not insights:
        insights.append("📈 **No significant emotional spikes. You're maintaining a steady emotional state.**")

    for insight in insights:
        st.markdown(insight)

    if show_raw_data:
        st.subheader("📜 Raw Log Entries")
        st.dataframe(df[['timestamp', 'window', 'text'] + melt_cols])
else:
    st.warning("No logs found. Please run the monitoring script first.")

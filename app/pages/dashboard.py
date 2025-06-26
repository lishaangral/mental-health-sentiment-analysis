import streamlit as st
import pandas as pd
import json
import os
import altair as alt

st.set_page_config(page_title="Mental Health Dashboard", layout="wide")
st.title("📊 Mental Health Sentiment Monitoring Dashboard")

log_file = "data/prediction_log.jsonl"

# Load and format logs
def load_logs(filepath):
    logs = []
    with open(filepath) as f:
        for line in f:
            try:
                log = json.loads(line)
                log["timestamp"] = pd.to_datetime(log.get("timestamp", pd.NaT))
                result = log.get("result", {})
                if isinstance(result, list):
                    for entry in result:
                        log[entry['label']] = entry['score']
                elif isinstance(result, dict):
                    log[result['label']] = result['score']
                logs.append(log)
            except json.JSONDecodeError:
                continue
    return pd.DataFrame(logs)

# Check for logs
if os.path.exists(log_file):
    df = load_logs(log_file)

    st.sidebar.header("⚙️ Settings")
    show_raw = st.sidebar.checkbox("Show Raw Data")

    st.subheader("📈 Sentiment Trends Over Time")

    if 'timestamp' not in df.columns:
        st.warning("⚠️ No 'timestamp' column found. Cannot plot trends.")
    else:
        labels = [col for col in df.columns if col not in ['timestamp', 'text', 'window', 'result']]
        if labels:
            for label in labels:
                line = alt.Chart(df).mark_line(point=True).encode(
                    x='timestamp:T',
                    y=alt.Y(label, scale=alt.Scale(domain=[0, 1])),
                    tooltip=['timestamp:T', label]
                ).properties(title=f"Sentiment Score for '{label}'", height=250)
                st.altair_chart(line, use_container_width=True)
        else:
            st.warning("No sentiment labels found to display.")

    st.subheader("📌 Score Summary")
    if labels:
        summary = df[labels].agg(['mean', 'max']).T.reset_index()
        summary.columns = ['Label', 'Average Score', 'Max Score']
        st.dataframe(summary.style.format("{:.2f}"))
    else:
        st.info("No scores available to summarize.")

    st.subheader("💡 Insight Highlights")
    insights = []
    for label in labels:
        if df[label].gt(0.8).sum() >= 3 and "neg" in label.lower():
            insights.append(f"🚨 High negative sentiment detected in **{label}**.")
        elif df[label].gt(0.85).sum() >= 3 and "pos" in label.lower():
            insights.append(f"😊 Positive sentiment trend in **{label}** looks great!")

    if insights:
        for note in insights:
            st.markdown(note)
    else:
        st.markdown("📊 You're maintaining a steady emotional profile.")

    if show_raw:
        st.subheader("🧾 Raw Logs")
        display_cols = ['timestamp', 'window', 'text'] + labels
        st.dataframe(df[display_cols], use_container_width=True)
else:
    st.warning("No prediction logs found. Run the sentiment monitor to collect data.")

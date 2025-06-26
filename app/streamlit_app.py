import streamlit as st
import pandas as pd
from cleanup import cleanup_old_logs
import json

# Load user settings
try:
    with open("../data/user_settings.json") as f:
        settings = json.load(f)
    retention_days = settings.get("log_retention_days", 7)
except:
    retention_days = 7  # default fallback

cleanup_old_logs(retention_days=retention_days)

# Page navigation
dashboard = st.Page("pages/dashboard.py", title="Dashboard", icon="📊")
monitor = st.Page("pages/monitor_settings.py", title="Monitor Settings", icon="⚙️")
notif = st.Page("pages/notification_settings.py", title="Notification Settings", icon="🔔")
sentiment = st.Page("pages/sentiment_control.py", title="Sentiment Control", icon="🧘")
thought = st.Page("pages/thought_input.py", title="Thoughts Check-in", icon="💆")

pg = st.navigation([dashboard, monitor, notif, sentiment, thought])
pg.run()

st.divider()

st.title("🌿 Mental Health Sentiment Analysis")

st.success("✅ Helping you stay emotionally aware, one screen at a time.")

# Layout: 2 columns
col1, col2 = st.columns(2)

with col1:
    st.header("How It Works?")
    st.markdown("""
    This app continuously **monitors emotional sentiment** by analyzing on-screen text from web-applications **you choose**.

    - Uses a **RoBERTa-based transformer model** fine-tuned for emotional and mental health analysis.
    - Captures text via **screenshot OCR** every few seconds and processes it securely on your device.
    - Logs predictions with timestamp and context for reflection and insights.
    """)

    st.info("🔐 **Your privacy is our top priority.** All data is stored locally. Nothing is uploaded, ever.")

    st.header("Personalize Your Experience.")
    st.markdown("""
    Use the **left sidebar** to:
    - Enable or disable screen monitoring
    - Pause sentiment tracking at any time
    - Toggle alerts for emotional triggers and daily check-ins
    - View real-time analytics in your **Dashboard**
    - Try calming tools in the **Sentiment Control** tab
                
    Note: Screen monitoring and related features will only work if you clone the repo and follow instructions given in README file.
    """)

with col2:
    st.header("What You Get?")
    st.markdown("#### **24/7 Emotional Insights**")
    st.markdown("- Track mood swings and emotional trends")
    st.markdown("- Identify stressful environments or content patterns")

    st.markdown("#### 🚨 **Distress Alerts**")
    st.markdown("- Be notified when signs of stress, anxiety, or sadness are detected")
    st.markdown("- Prompted with relaxing activities when needed")

    st.markdown("#### **Positive Reinforcement**")
    st.markdown("- Celebrate positive emotional spikes")
    st.markdown("- Stay motivated with joyful feedback")

    st.success("💡 Great for students, remote workers or anyone curious about their digital emotional wellbeing.")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Streamlit, Transformers and a vision for proactive mental health care.")

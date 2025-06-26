# Allows users to enter text and recieve real time sentiment analysis

import streamlit as st
from scripts.predict_pipeline import analyze_text
import datetime
import json
import os

SETTINGS_FILE = "../data/user_settings.json"
LOG_FILE = "../data/prediction_log.jsonl"

st.set_page_config(page_title="Thoughts Check-in", layout="centered")
st.title("Thoughts Check-in")
st.header("Write away what you feel and we'll help you analyse your thoughts.")

st.markdown("""
This space is for you to express how you're feeling.
Type a thought, concern, or even a random reflection.
We'll help you analyze the sentiment and suggest resources to support you.
""")

user_input = st.text_area("✍️ How are you feeling right now?", height=150)

if st.button("Analyze My Thought") and user_input.strip():
    result = analyze_text(user_input)
    st.subheader("📊 Sentiment Analysis Result")
    st.write(result)

    # save to log
    log = {
        "timestamp": datetime.datetime.now().isoformat(),
        "window": "Manual Input",
        "text": user_input[:200],
        "result": result
    }

    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log) + "\n")

    # sisplay feedback
    label = result.get("label", "").lower()
    score = result.get("score", 0)

    if label in ["sad", "distress", "anger", "anxious"] and score >= 0.75:
        st.warning("🚨 You seem distressed. Would you like to visit the Sentiment Control page?")
        if st.button("Go to Sentiment Control"):
            st.switch_page("pages/sentiment_control.py")
    elif label in ["joy", "positive", "happy"] and score >= 0.75:
        st.success("😊 That's wonderful to hear! Keep going.")
    else:
        st.info("We're here for you no matter what. Feel free to check the dashboard for patterns over time.")

else:
    st.caption("This will log your sentiment and help you track your emotional journey.")

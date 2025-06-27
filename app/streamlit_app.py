import streamlit as st
from transformers import pipeline

# Load model
model_name = "lishaangral/roberta-mental-health"
classifier = pipeline("text-classification", model=model_name, tokenizer=model_name, framework="pt", truncation=True, max_length=512)

# Extended subcategories based on prediction confidence
subcategory_map = {
    "Suicidal": [
        (0.0, 0.2, "Vague Thoughts"),
        (0.2, 0.4, "Negative Ideation"),
        (0.4, 0.6, "Intense Hopelessness"),
        (0.6, 0.8, "Severe Crisis Symptoms"),
        (0.8, 1.0, "Critical Danger State")
    ],
    "Depression": [
        (0.0, 0.2, "Mild Blues"),
        (0.2, 0.4, "Emotional Fatigue"),
        (0.4, 0.6, "Recurring Sadness"),
        (0.6, 0.8, "Clinical Low"),
        (0.8, 1.0, "Severe Depression Episode")
    ],
    "Anxiety": [
        (0.0, 0.2, "Mild Tension"),
        (0.2, 0.4, "Cognitive Worry"),
        (0.4, 0.6, "Nervous Anticipation"),
        (0.6, 0.8, "Panic Symptoms"),
        (0.8, 1.0, "High Alert Anxiety")
    ],
    "Stress": [
        (0.0, 0.2, "Everyday Pressure"),
        (0.2, 0.4, "Task Overload"),
        (0.4, 0.6, "Emotional Overwhelm"),
        (0.6, 0.8, "Chronic Strain"),
        (0.8, 1.0, "Severe Burnout Risk")
    ],
    "Normal": [
        (0.0, 1.0, "What you're feeling is highly likely to be normal"),
    ],
    "Bi-Polar": [
        (0.0, 0.3, "Mild Shifts"),
        (0.3, 0.6, "Mood Inconsistencies"),
        (0.6, 0.8, "Episode Suspected"),
        (0.8, 1.0, "High-Risk Cycle Detected")
    ],
    "Personality Disorder": [
        (0.0, 0.3, "Slight Behavioral Traits"),
        (0.3, 0.6, "Pattern Recognition Needed"),
        (0.6, 0.8, "Personality Indicators"),
        (0.8, 1.0, "Strong Personality Deviance")
    ]
}

# UI Setup
st.set_page_config(page_title="🌱 Mental Health Sentiment Analyzer", layout="centered")
st.markdown("""
    <style>
        .stApp {
            font-family: 'Segoe UI', sans-serif;]
        }
    </style>
""", unsafe_allow_html=True)

# App Title and Description
st.title("🌿 Mental Health Sentiment Analyzer")
st.markdown("""
This tool helps you reflect on your current emotional state using an AI model trained on real mental health conversations.  
Type your feelings below. The app will detect your emotion and break it down into finer emotional nuances.

🔒 <i>Your input is not saved or shared.</i>
""", unsafe_allow_html=True)

# Text Input
user_input = st.text_area("How are you feeling today?", height=150)

# Analyze Button
if st.button("🩺 Analyze My Emotions"):
    if user_input.strip():
        results = classifier(user_input)
        st.subheader("🧾 Full Emotion Report")

        for res in results:
            label = res['label']
            score = res['score']
            percentage = score * 100

            # Find subcategory
            subclass = "Uncertain"
            for lower, upper, sub in subcategory_map.get(label, []):
                if lower <= score < upper:
                    subclass = sub
                    break

            st.markdown(f"**Primary Emotion:** `{label}` ({percentage:.2f}%)")
            st.markdown(f"**Subcategory:** {subclass}")
            st.markdown("---")
    else:
        st.warning("Please enter some thoughts to analyze.")

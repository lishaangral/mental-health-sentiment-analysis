import streamlit as st
from transformers import pipeline
import torch
import matplotlib.pyplot as plt

# Set model name and device
model_name = "lishaangral/roberta-mental-health-v2"
device = 0 if torch.cuda.is_available() else -1

# Initialize pipeline
classifier = pipeline(
    "text-classification",
    model=model_name,
    tokenizer=model_name,
    device=device,
    return_all_scores=True,
    top_k=None,
    truncation=True,
    max_length=512
)

# Label list (capitalized)
label_list = [
    "Admiration", "Amusement", "Anger", "Annoyance", "Approval", "Caring", "Confusion", "Curiosity",
    "Desire", "Disappointment", "Disapproval", "Disgust", "Embarrassment", "Excitement", "Fear",
    "Gratitude", "Grief", "Joy", "Love", "Nervousness", "Optimism", "Pride", "Realization", "Relief",
    "Remorse", "Sadness", "Surprise", "Neutral"
]

# UI
st.set_page_config(page_title="🌱 Mental Health Sentiment Analyzer", layout="centered")
st.title("🌿 Mental Health Sentiment Analyzer")
st.markdown("""
This tool analyzes the emotional tone in your writing and shows you a breakdown of emotions detected by the model.

🔒 <i>Your input is not saved or shared.</i>
""", unsafe_allow_html=True)

user_input = st.text_area("How are you feeling today?", height=150)

if st.button("🩺 Analyze Emotions & Show Chart"):
    if user_input.strip():
        with st.spinner("Analyzing..."):
            results = classifier(user_input)[0]

            # Map "LABEL_x" to actual emotion
            sentiment_scores = {
                label_list[int(entry["label"].split("_")[-1])]: entry["score"]
                for entry in results
            }

            # Sort scores
            sorted_data = sorted(sentiment_scores.items(), key=lambda x: x[1], reverse=True)

            # Show strong emotions
            st.subheader("Strongest Emotions Detected (Score > 30%)")
            strong = [(label, f"{score * 100:.2f}%") for label, score in sorted_data if score > 0.3]
            if strong:
                for label, score in strong:
                    st.markdown(f"- **{label}**: {score}")
            else:
                st.info("No dominant emotional signals detected.")

            # Show chart
            st.subheader("📊 Sentiment Composition Chart (Top 10)")
            top_scores_dict = dict(sorted_data[:10])
            fig, ax = plt.subplots()
            ax.barh(list(top_scores_dict.keys()), list(top_scores_dict.values()), color='skyblue')
            ax.invert_yaxis()
            ax.set_xlabel("Score")
            ax.set_title("Top 10 Emotion Probabilities")
            st.pyplot(fig)

    else:
        st.warning("Please enter some text to analyze.")

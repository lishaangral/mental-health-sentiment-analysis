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
    top_k=None,  # get all labels
    truncation=True,
    max_length=512
)

# Define label list in the correct order
label_list = [
    "Admiration", "Amusement", "Anger", "Annoyance", "Approval", "Caring", "Confusion", "Curiosity",
    "Desire", "Disappointment", "Disapproval", "Disgust", "Embarrassment", "Excitement", "Fear",
    "Gratitude", "Grief", "Joy", "Love", "Nervousness", "Optimism", "Pride", "Realization", "Relief",
    "Remorse", "Sadness", "Surprise", "Neutral"
]

# Streamlit UI
st.set_page_config(page_title="🌱 Mental Health Sentiment Analyzer", layout="centered")
st.title("🌿 Mental Health Sentiment Analyzer")
st.markdown("""
This tool analyzes the emotional tone in your writing and shows you a breakdown of emotions detected by the model.

🔒 <i>Your input is not saved or shared.</i>
""", unsafe_allow_html=True)

# Text Input
user_input = st.text_area("How are you feeling today?", height=150)

# Analyze Button
if st.button("🩺 Analyze My Emotions"):
    if user_input.strip():
        results = classifier(user_input)[0]  # Get list of dicts for each label

        # Extract scores
        scores = [entry['score'] for entry in results]

        # Sort labels and scores by score descending
        sorted_data = sorted(zip(label_list, scores), key=lambda x: x[1], reverse=True)
        top_labels, top_scores = zip(*sorted_data)

    # Visualize top sentiments
if st.button("📊 Show Sentiment Composition Chart"):
    with st.spinner("Generating chart..."):
        sentiment_scores = {entry['label'].title(): entry['score'] for entry in results}

        sorted_scores = dict(sorted(sentiment_scores.items(), key=lambda x: x[1], reverse=True)[:10])

        fig, ax = plt.subplots()
        ax.barh(list(sorted_scores.keys()), list(sorted_scores.values()), color='skyblue')
        ax.invert_yaxis()
        ax.set_xlabel('Score')
        ax.set_title('Top 10 Emotion Probabilities')
        st.pyplot(fig)

        # Optionally: also show high-confidence emotions (>0.3)
        st.subheader("Strongest Emotions Detected (Score > 30%)")
        strong = [(label, f"{score*100:.2f}%") for label, score in sorted_data if score > 0.3]
        if strong:
            for label, score in strong:
                st.markdown(f"- **{label.title()}**: {score}")
        else:
            st.info("No dominant emotional signals detected.")
    else:
        st.warning("Please enter some thoughts to analyze.")

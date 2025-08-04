import streamlit as st
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import torch
import matplotlib.pyplot as plt

# Set model name and device
model_name = "lishaangral/roberta-mental-health-v2"
device = "cuda" if torch.cuda.is_available() else "cpu"

model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Initialize pipeline
classifier = pipeline(
    "text-classification",
    model=model,
    tokenizer=tokenizer,
    device=0 if device == "cuda" else -1,
    return_all_scores=True
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
            raw_results = classifier(user_input, truncation=True, max_length=512)[0]

            # Map "LABEL_x" to actual emotion
            sentiment_scores = {
                label_list[int(entry["label"].split("_")[-1])]: entry["score"]
                for entry in raw_results
            }

            # Sort scores
            sorted_emotions = sorted(sentiment_scores.items(), key=lambda x: x[1], reverse=True)

            # Show strong emotions
            st.subheader("Strongest Emotions Detected (Score > 30%)")
            strong = [(label, f"{score * 100:.2f}%") for label, score in sorted_emotions if score > 0.3]
            if strong:
                for label, score in strong:
                    st.markdown(f"- **{label}**: {score}")
            else:
                st.info("No dominant emotional signals detected.")

            # Show chart
            st.subheader("📊 Sentiment Composition Chart (Top 10)")
            top10 = dict(sorted_emotions[:10])
            fig, ax = plt.subplots(figsize=(6, 4))
            bars = ax.barh(list(top10.keys()), list(top10.values()), color='skyblue')
            ax.invert_yaxis()
            ax.set_xlabel("Score")
            ax.set_xlim(0, 1)
            ax.set_title("Top 10 Emotion Probabilities")

            # Add percentage labels on bars
            for bar in bars:
                width = bar.get_width()
                ax.text(width + 0.01, bar.get_y() + bar.get_height()/2,
                        f"{width*100:.1f}%", va='center')

            st.pyplot(fig)

    else:
        st.warning("Please enter some text to analyze.")

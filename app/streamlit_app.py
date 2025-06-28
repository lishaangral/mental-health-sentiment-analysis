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

        # Extract label-score mapping and sort
        sentiment_scores = {entry['label'].title(): entry['score'] for entry in results}
        sorted_data = sorted(sentiment_scores.items(), key=lambda x: x[1], reverse=True)
        top_labels, top_scores = zip(*sorted_data)

        # Optionally: show strong signals
        st.subheader("Strongest Emotions Detected (Score > 30%)")
        strong = [(label, f"{score * 100:.2f}%") for label, score in sorted_data if score > 0.3]
        if strong:
            for label, score in strong:
                st.markdown(f"- **{label}**: {score}")
        else:
            st.info("No dominant emotional signals detected.")

        # Show composition chart
        if st.button("📊 Show Sentiment Composition Chart"):
            with st.spinner("Generating chart..."):
                top_n = 10  # Show top 10 emotions
                top_scores_dict = dict(sorted_data[:top_n])

                fig, ax = plt.subplots()
                ax.barh(list(top_scores_dict.keys()), list(top_scores_dict.values()), color='skyblue')
                ax.invert_yaxis()
                ax.set_xlabel('Score')
                ax.set_title('Top 10 Emotion Probabilities')
                st.pyplot(fig)

    else:
        st.warning("Please enter some thoughts to analyze.")

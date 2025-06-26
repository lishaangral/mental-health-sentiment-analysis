# Defines how the text input will be analyzed and divided into tokens and chunks to predict on larger text inputs

from transformers import pipeline
from collections import defaultdict
from transformers import AutoTokenizer, AutoModelForSequenceClassification


# load fine-tuned model and tokenizer
sentiment_pipeline = pipeline(
    "text-classification",
    model = AutoModelForSequenceClassification.from_pretrained("lishaangral/roberta-mental-health"),
    tokenizer = AutoTokenizer.from_pretrained("lishaangral/roberta-mental-health"),
    truncation=True,
    top_k=None
)
from collections import defaultdict

def analyze_text(text, max_length=512, stride=256):
    tokenizer = sentiment_pipeline.tokenizer
    model = sentiment_pipeline.model

    # Tokenize and chunk input text
    tokens = tokenizer(text, return_tensors='pt', truncation=False)['input_ids'][0]
    chunks = [tokens[i:i + max_length] for i in range(0, len(tokens), stride)]

    label_scores = defaultdict(float)
    results = []

    for chunk in chunks:
        decoded = tokenizer.decode(chunk, skip_special_tokens=True)

        # Get prediction
        chunk_result = sentiment_pipeline(decoded)

        # Handle case where result is a list
        if chunk_result and isinstance(chunk_result, list):
            result = chunk_result[0]  # Get top result
            label = result['label']
            score = result['score']
            label_scores[label] += score
            results.append({"chunk": decoded[:100], "label": label, "score": score})

    # Sort aggregated label scores
    sorted_labels = sorted(label_scores.items(), key=lambda x: x[1], reverse=True)

    return {
        "summary": sorted_labels,
        "details": results
    }

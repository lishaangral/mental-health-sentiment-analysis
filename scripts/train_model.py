'''NOTE: This is the code used to fine-tune the pre-trained roberta model on labelled dataset 'https://www.kaggle.com/datasets/suchintikasarkar/sentiment-analysis-for-mental-health'
   The model was fine-tuned on GPU using Google Colabs and then uploaded to HuggingFace. '''

from datasets import Dataset
from transformers import RobertaTokenizer, RobertaForSequenceClassification, TrainingArguments, Trainer
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

# load your dataset
csv_path = "../data/mental_health_dataset.csv"
df = pd.read_csv(csv_path)

# map text labels (e.g., Anxiety) to integers
label2id = {label: idx for idx, label in enumerate(sorted(df["status"].unique()))}
id2label = {v: k for k, v in label2id.items()}

df = df.dropna(subset=["statement", "status"])

# add numeric label column
df["label"] = df["status"].map(label2id)

# prepare Hugging Face dataset
dataset = Dataset.from_pandas(df[["statement", "label"]])

# tokenization
model_ckpt = "roberta-base"
tokenizer = RobertaTokenizer.from_pretrained(model_ckpt)

def preprocess_function(examples):
    # ensure all statements are strings and not None
    texts = [str(x) if x is not None else "" for x in examples["statement"]]
    return tokenizer(texts, truncation=True, padding=True)

tokenized_dataset = dataset.train_test_split(test_size=0.2)
tokenized_dataset = tokenized_dataset.map(preprocess_function, batched=True)

# load and configure model
model = RobertaForSequenceClassification.from_pretrained(
    model_ckpt,
    num_labels=len(label2id),
    id2label=id2label,
    label2id=label2id
)
# trainingArguments + trainer
def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(axis=-1)
    return {
        "accuracy": accuracy_score(labels, preds),
        "f1": f1_score(labels, preds, average='weighted')
    }

# Training arguments
training_args = TrainingArguments(
    output_dir="./roberta-mental-health",
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    num_train_epochs=3,
    eval_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    weight_decay=0.01,
    logging_dir="./logs",
    fp16=True # used with GPU
)

# Trainer setup
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# train and save
trainer.train()

# commented out because we'll be using our own uploaded HuggingFace API
# model.save_pretrained("../models/roberta-mental-health")
# tokenizer.save_pretrained("../models/roberta-mental-health") 
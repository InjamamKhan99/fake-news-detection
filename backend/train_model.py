import pandas as pd
import numpy as np
import joblib
import logging
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import DistilBertTokenizer, DistilBertModel
import torch

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load datasets
true_df = pd.read_csv("backend/dataset/true.csv")
fake_df = pd.read_csv("backend/dataset/fake.csv")

true_df["label"] = 0  # Real news
fake_df["label"] = 1  # Fake news

# Combine datasets
df = pd.concat([true_df, fake_df], ignore_index=True)

# Load feedback data
feedback_path = "backend/feedback_data.csv"
try:
    feedback_df = pd.read_csv(feedback_path)
    if not feedback_df.empty:
        df = pd.concat([df, feedback_df], ignore_index=True)
        logging.info("Feedback data incorporated into training dataset.")
    else:
        logging.info("Feedback data is empty. Skipping feedback integration.")
except FileNotFoundError:
    logging.warning("Feedback data file not found. Proceeding without feedback data.")

# Preprocessing
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
bert_model = DistilBertModel.from_pretrained("distilbert-base-uncased")

def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy().flatten()

# Generate embeddings
df["bert_embeddings"] = df["text"].apply(get_bert_embeddings)

# TF-IDF Feature Extraction
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_tfidf = vectorizer.fit_transform(df["text"])

# Combine TF-IDF & BERT embeddings
X_combined = np.hstack((X_tfidf.toarray(), np.vstack(df["bert_embeddings"])))
y = df["label"].values

# Train Hybrid Model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_combined, y)

# Save model
joblib.dump(clf, "backend/hybrid_fake_news_model.pkl")
joblib.dump(vectorizer, "backend/one_hot_encoder.pkl")

logging.info("Model retrained and saved successfully.")

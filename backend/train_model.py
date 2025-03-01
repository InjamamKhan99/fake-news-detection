import pandas as pd
import numpy as np
import joblib
import logging
import warnings
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from transformers import DistilBertTokenizer, DistilBertModel
import torch
from tqdm import tqdm  # For progress tracking

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Suppress FutureWarnings
warnings.simplefilter(action="ignore", category=FutureWarning)

# Load datasets
true_df = pd.read_csv(r"dataset/true.csv")
fake_df = pd.read_csv(r"dataset/fake.csv")

true_df["label"] = 0  # Real news
fake_df["label"] = 1  # Fake news

df = pd.concat([true_df, fake_df], ignore_index=True)

# Load feedback data if available
feedback_path = "feedback_data.csv"
if os.path.exists(feedback_path):
    try:
        feedback_df = pd.read_csv(feedback_path)
        if not feedback_df.empty:
            feedback_df.rename(columns={"news_text": "text", "correct": "label"}, inplace=True)  # Fix column names
            df = pd.concat([df, feedback_df], ignore_index=True)
            logging.info("Feedback data incorporated into training dataset.")
        else:
            logging.info("Feedback data is empty. Skipping feedback integration.")
    except pd.errors.EmptyDataError:
        logging.warning("Feedback data file exists but is empty. Proceeding without feedback data.")
else:
    logging.warning("Feedback data file not found. Proceeding without feedback data.")

# Ensure all text is a string (avoid NaN issues)
df["text"] = df["text"].astype(str).fillna("")

# Load BERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
bert_model = DistilBertModel.from_pretrained("distilbert-base-uncased")

def get_bert_embeddings(text_list):
    """Batch process text inputs to generate BERT embeddings."""
    inputs = tokenizer(text_list, padding=True, truncation=True, max_length=512, return_tensors="pt")
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy()

# Process text in batches
batch_size = 16
bert_embeddings = []
for i in tqdm(range(0, len(df), batch_size), desc="Generating BERT Embeddings"):
    batch_texts = df["text"][i : i + batch_size].tolist()
    bert_embeddings.append(get_bert_embeddings(batch_texts))

bert_embeddings = np.vstack(bert_embeddings)

# TF-IDF Feature Extraction
vectorizer = TfidfVectorizer(stop_words="english", max_features=5000)
X_tfidf = vectorizer.fit_transform(df["text"])

# Combine TF-IDF & BERT embeddings
X_combined = np.hstack((X_tfidf.toarray(), bert_embeddings))
y = df["label"].values

# Train Hybrid Model
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_combined, y)

# Ensure backend folder exists for saving models
os.makedirs("backend", exist_ok=True)

# Save the trained model and vectorizer
joblib.dump(clf, r"hybrid_fake_news_model.pkl")
joblib.dump(vectorizer, r"tfidf_vectorizer.pkl")

logging.info("Model retrained and saved successfully.")

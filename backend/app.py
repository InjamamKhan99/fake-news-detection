import os
import uvicorn
import pandas as pd
import joblib
import torch
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import DistilBertTokenizer, DistilBertModel
from fact_checking import fact_check_news  
from source_credibility import check_source_credibility

# Initialize FastAPI app
app = FastAPI()

# Load models
MODEL_PATH = "backend/hybrid_fake_news_model.pkl"
VECTORIZER_PATH = "backend/tfidf_vectorizer.pkl"  # Fixed variable name

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
bert_model = DistilBertModel.from_pretrained("distilbert-base-uncased")
model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)  # Load TF-IDF vectorizer

FEEDBACK_FILE = "backend/feedback_data.csv"

# Define request format
class NewsRequest(BaseModel):
    news_text: str

class FeedbackRequest(BaseModel):
    news_text: str
    correct: bool

def get_bert_embeddings(text):
    """Generate BERT embeddings for input text."""
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = bert_model(**inputs)
    return outputs.last_hidden_state[:, 0, :].numpy().flatten()

@app.post("/predict")
def predict(news: NewsRequest):
    """Predicts whether a news article is fake or real."""
    try:
        # Generate BERT embeddings
        bert_features = get_bert_embeddings(news.news_text).reshape(1, -1)
        
        # Generate TF-IDF features
        tfidf_features = vectorizer.transform([news.news_text]).toarray()

        # Combine TF-IDF & BERT embeddings (Fixed the combination issue)
        X_combined = np.hstack((tfidf_features, bert_features))

        # Make prediction
        prediction = model.predict(X_combined)
        return {"fake": bool(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/fact-check")
def fact_check(news: NewsRequest):
    """Uses Google Fact Check API to verify news claims."""
    return fact_check_news(news.news_text)  

@app.post("/source-credibility")
def source_credibility(news: NewsRequest):
    """Checks the credibility of the news source."""
    return check_source_credibility(news.news_text)

@app.post("/feedback")
def feedback(feedback_data: FeedbackRequest):
    """Stores user feedback for automated retraining."""
    df = pd.DataFrame([[feedback_data.news_text, int(feedback_data.correct)]], columns=["text", "label"])  
    df.to_csv(FEEDBACK_FILE, mode='a', header=not os.path.exists(FEEDBACK_FILE), index=False)
    return {"message": "Feedback recorded"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
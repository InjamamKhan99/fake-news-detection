import os
import uvicorn
import pandas as pd
import joblib
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import DistilBertTokenizer, DistilBertModel
from fact_checking import fact_check_news  # Updated import
from source_credibility import check_source_credibility
from train_model import retrain_model  # Import retraining function

# Initialize FastAPI app
app = FastAPI()

# Load models
MODEL_PATH = "backend/hybrid_fake_news_model.pkl"
ENCODER_PATH = "backend/one_hot_encoder.pkl"

tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
bert_model = DistilBertModel.from_pretrained("distilbert-base-uncased")
model = joblib.load(MODEL_PATH)
encoder = joblib.load(ENCODER_PATH)

FEEDBACK_FILE = "backend/feedback_data.csv"

# Define request format
class NewsRequest(BaseModel):
    news_text: str

class FeedbackRequest(BaseModel):
    news_text: str
    correct: bool

@app.post("/predict")
def predict(news: NewsRequest):
    """Predicts whether a news article is fake or real."""
    try:
        tokens = tokenizer(news.news_text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            embeddings = bert_model(**tokens).last_hidden_state[:, 0, :].numpy()
        prediction = model.predict(embeddings)
        return {"fake": bool(prediction[0])}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/fact-check")
def fact_check(news: NewsRequest):
    """Uses Google Fact Check API to verify news claims."""
    return fact_check_news(news.news_text)  # Updated function call

@app.post("/source-credibility")
def source_credibility(news: NewsRequest):
    """Checks the credibility of the news source."""
    return check_source_credibility(news.news_text)

@app.post("/feedback")
def feedback(feedback_data: FeedbackRequest):
    """Stores user feedback for automated retraining."""
    df = pd.DataFrame([[feedback_data.news_text, feedback_data.correct]], columns=["news_text", "correct"])
    df.to_csv(FEEDBACK_FILE, mode='a', header=not os.path.exists(FEEDBACK_FILE), index=False)
    return {"message": "Feedback recorded"}

@app.post("/retrain")
def retrain():
    """Retrains the model using feedback data."""
    if not os.path.exists(FEEDBACK_FILE) or os.stat(FEEDBACK_FILE).st_size == 0:
        raise HTTPException(status_code=400, detail="No feedback data available")
    retrain_model(FEEDBACK_FILE, MODEL_PATH)
    return {"message": "Model retrained successfully"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
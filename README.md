# Fake News Detection System

## Overview
This project is a **Fake News Detection System** that classifies news articles as **Fake or Real** using a hybrid machine learning approach.

The system combines **BERT embeddings**, **Random Forest classifier**, and **metadata-based features** to improve prediction accuracy. It also integrates the **Google Fact Check API** for real-time verification and includes a feedback mechanism for continuous model improvement.

---

## Features

- Fake News Detection using a trained ML model  
- Real-time fact-checking using **Google Fact Check API**  
- User feedback system to improve model accuracy  
- Automated model retraining when enough feedback data is collected  
- Docker and Kubernetes support for deployment  

---

## Tech Stack

- Python
- FastAPI
- Scikit-learn
- BERT Embeddings
- Pandas & NumPy
- HTML, CSS, JavaScript
- Docker
- Kubernetes

---

## Project Structure

```
fake_news_detection_system/
│
├── backend/
│   ├── app.py
│   ├── dataset/
│   │   ├── fake.csv
│   │   └── true.csv
│   ├── fact_checking.py
│   ├── source_credibility.py
│   ├── train_model.py
│   ├── feedback_data.csv
│   ├── one_hot_encoder.pkl
│   ├── hybrid_fake_news_model.pkl
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── deployment/
│   ├── Dockerfile
│   └── kubernetes.yaml
│
├── .env
├── .gitignore
└── README.md
```
## Installation & Setup

### 1️. Clone the Repository

```bash
git clone https://github.com/InjamamKhan99/fake-news-detection.git
cd fake-news-detection
```
### 2️. Create Virtual Environment

#### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```
### 3️. Install Dependencies

```bash
pip install -r backend/requirements.txt
```
### 4️. Set Up Environment Variables

Create a `.env` file in the project root and add the following:

```env
GOOGLE_FACT_CHECK_API_KEY=your-google-api-key
PYTHONPATH=/app/backend
```
5️. Run the Backend
cd backend
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
6️. Run the Frontend

Open the file below in a browser:

frontend/index.html
Docker Deployment
Build Docker Image
docker build -t fake-news-api .
Run Docker Container
docker run -p 8000:8000 fake-news-api
Kubernetes Deployment
kubectl apply -f deployment/kubernetes.yaml
Future Improvements

Improve model accuracy using deep learning models
Add a full React frontend
Deploy the system on a cloud platform

Author
Injamam Khan
B.Tech Computer Science and Engineering
Machine Learning & Data Science Enthusiast

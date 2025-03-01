Fake News Detection System
Project Overview
This project is a Fake News Detection System that uses a hybrid model (BERT embeddings + Random Forest + metadata features) to classify news as Fake or Real. It integrates Google Fact Check API for real-time fact-checking and supports automated model retraining based on user feedback.

Features
✅ Fake News Detection using a trained ML model
✅ Real-time Fact-Checking using Google Fact Check API
✅ Feedback Mechanism for users to improve model accuracy
✅ Automated Model Retraining when sufficient feedback data is collected
✅ Docker & Kubernetes Support for easy deployment

Project Structure

fake_news_detection_system/
│-- backend/
│   ├── app.py
│   ├── dataset/
│   │   ├── fake.csv
│   │   ├── true.csv
│   ├── fact_checking.py
│   ├── source_credibility.py
│   ├── train_model.py
│   ├── feedback_data.csv
│   ├── one_hot_encoder.pkl
│   ├── hybrid_fake_news_model.pkl
│   ├── requirements.txt
│
│-- frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│
│-- deployment/
│   ├── Dockerfile
│   ├── kubernetes.yaml
│
│-- .env  # Stores API Keys (Not included in Git)
│-- .gitignore  # Prevents sensitive files from being committed
│-- README.md  # Project Documentation
Installation & Setup
1️⃣ Clone the Repository

git clone https://github.com/InjamamKhan99/fake-news-detection.git  
cd fake-news-detection
2️⃣ Set Up Virtual Environment (Recommended)

For macOS & Linux

python3 -m venv venv  
source venv/bin/activate  
For Windows (Command Prompt or PowerShell)

python -m venv venv  
venv\Scripts\activate
3️⃣ Install Dependencies

pip install -r backend/requirements.txt
4️⃣ Set Up Environment Variables
Create a .env file in the project root and add your API key:


GOOGLE_FACT_CHECK_API_KEY=your-google-api-key
PYTHONPATH=/app/backend  # Ensures FastAPI finds backend modules
5️⃣ Run the Backend

cd backend  
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
6️⃣ Run the Frontend
Simply open frontend/index.html in a browser.

Docker & Kubernetes Deployment (Optional)
1️⃣ Build & Run Docker Container

docker build -t fake-news-api .
docker run -p 8000:8000 fake-news-api
2️⃣ Deploy with Kubernetes

kubectl apply -f deployment/kubernetes.yaml
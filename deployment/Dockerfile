FROM python:3.9

# Set working directory
WORKDIR /app

# Set PYTHONPATH so FastAPI finds backend
ENV PYTHONPATH="/app/backend"

# Copy project files
COPY backend/requirements.txt .  
COPY backend /app/backend
COPY frontend /app/frontend

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download Hugging Face models (BERT)
RUN python -c "from transformers import DistilBertTokenizer, DistilBertModel; \
    DistilBertTokenizer.from_pretrained('distilbert-base-uncased'); \
    DistilBertModel.from_pretrained('distilbert-base-uncased')"

# Expose FastAPI port
EXPOSE 8000

# Command to run FastAPI server
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]

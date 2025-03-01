FROM python:3.9 

# Set working directory
WORKDIR /app

# Set PYTHONPATH so FastAPI finds backend
ENV PYTHONPATH="/app/backend"

# Copy project files
COPY backend/requirements.txt /app/requirements.txt
COPY backend /app/backend
COPY backend/dataset /app/backend/dataset  # Ensure dataset is included
COPY frontend /app/frontend
COPY .env /app/  # Copy .env file

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Ensure feedback_data.csv exists
RUN touch /app/backend/feedback_data.csv

# Download Hugging Face models (BERT)
RUN python -c "from transformers import DistilBertTokenizer, DistilBertModel; \
    DistilBertTokenizer.from_pretrained('distilbert-base-uncased'); \
    DistilBertModel.from_pretrained('distilbert-base-uncased')"

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI server with multiple workers
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
# Use official Python image
FROM python:3.10-slim

WORKDIR /app

# Copy requirements first (better caching)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy remaining files
COPY . .

# Expose Flask port
EXPOSE 5000

# Run Flask app properly
CMD ["python", "app.py"]

# Base image
FROM python:3.11-slim

# Prevent Python from writing pyc files
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    build-essential \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for caching)
COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m nltk.downloader punkt punkt_tab

# Copy project
COPY . /app/

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# Roshan – Document-Based Question Answering System
## Overview
Roshan is a backend system that provides document-aware question answering using:
* Django (REST API)
* PostgreSQL
* Vector similarity search (FAISS)
* LangChain
* Open-source LLMs via Hugging Face API

The system allows you to:
1. Store documents with tags
2. Automatically generate document summaries
3. Build vector embeddings for semantic search
4. Retrieve relevant documents when a question is submitted
5. Combine retrieved documents with the question
6. Generate an answer using a free open-source LLM
This project demonstrates a Retrieval-Augmented Generation (RAG) pipeline.
___
## Architecture
The question-answering flow:
```
User Question
      ↓
Retrieve Related Documents (Vector Search)
      ↓
Combine Question + Retrieved Context
      ↓
Generate Answer via LLM (Hugging Face)
      ↓
Return Response
```
___
## Screenshot
![Admin Dashboard](./dashboard.png?raw=true)
![Documnets List](./document.png?raw=true)
![Questions List](./question.png?raw=true)
___
## Setup Guide (Linux)
### 1. Clone the Repository
```Bash
git clone https://github.com/MJ-MN/Roshan.git
cd roshan
```
### 2. Create a Virtual Environment
```Bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```Bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist yet:
```Bash
pip install django djangorestframework psycopg2-binary
pip install langchain langchain-community langchain-huggingface
pip install sentence-transformers faiss-cpu
pip install huggingface_hub python-dotenv
```
___
## PostgreSQL Configuration
### 1. Install PostgreSQL
```Bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### 2. Create Database
```Bash
sudo -u postgres psql
```
Inside PostgreSQL:
```SQL
CREATE DATABASE roshan_db;
CREATE USER roshan_user WITH PASSWORD 'yourpassword';
ALTER ROLE roshan_user SET client_encoding TO 'utf8';
ALTER ROLE roshan_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE roshan_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE roshan_db TO roshan_user;
\q
```
___
## Environment Variables
Create a `.env` file in the project root:
```
DB_NAME=roshan_db
DB_USER=roshan_user
DB_PASSWORD=yourpassword
DB_HOST=localhost
DB_PORT=5432
```
___
## Run the Project
### 1. Apply Migrations
```Bash
python manage.py makemigrations
python manage.py migrate
```
### 2. Create Superuser
```Bash
python manage.py createsuperuser
```
### 3. Run the Development Server
```Bash
python manage.py runserver
```
Visit:
```
http://127.0.0.1:8000/admin/
```
___
## How to Use the System
### Step 1 – Add a Tag
1. Go to Django Admin.
2. Click "Tags".
3. Add a new tag.
3. Save.

Tags help categorize documents.

### Step 2 – Add a Document
1. Go to "Documents".
2. Click "Add Document".
3. Add:
    * Title
    * Content
    * Tag
4. Click Save.

### Automatic Summary Generation
When a document is saved:
* The content is processed using the `sumy` library
* The **TextRank** algorithm generates an extractive summary
* The summary field is automatically populated

The summary generation is fully local and does **not** use the LLM API.

### Step 3 – Build Embeddings
After inserting documents, build embeddings for semantic search.
Run:
```Bash
python manage.py build_embeddings
```
This command:
* Converts document content into vector embeddings
* Stores them in FAISS
* Enables similarity search

If you do not build embeddings, retrieval will not work.

### Step 4 – Register a Question (POST API)
Use Postman or curl.
Endpoint:
```
POST /questions/
```
Example request:
```JSON
{
    "question_text": "What is LangChain used for?"
}
```
Example curl:
```Bash
curl -X POST http://127.0.0.1:8000/questions/ \
     -H "Content-Type: application/json" \
     -d '{"question_text": "What is LangChain used for?"}'
```
___
## What Happens Internally
When a question is submitted:
1. The question is saved in the database.
2. The system retrieves relevant documents using FAISS.
3. The question and document contents are merged.
4. A prompt is constructed.
5. The prompt is sent to the Hugging Face LLM.
6. The generated answer is saved and returned.

The question object includes:
* The related document (clickable in admin)
* The generated answer
___
## Example Response
```JSON
{
    "id": 47,
    "question_text": "What is an one-dimensional electronic structure?",
    "related_documents": [
        "Title: document title 1\n            Content: document content 1",
        "Title: document title 2\n            Content: document content 2"
    ],
    "answer": "phosphorus chains"
}
```
___
## Project Structure
```
roshan/
│
├── config/
|   |
|   ├── settings/
|   |   |
|   |   └── base.py
|   |
|   ├── asgi.py
|   ├── urls.py
|   └── wsgi.py
|
├── roshan_ai/
|   |
|   ├── management/
|   |   |
|   |   └── commands/
|   |       |
|   |       └── build_embeddings.py
|   |
|   ├── services/
|   |   |
│   |   ├── martcher.py
|   |   ├── rag.py
|   |   ├── retriever.py
|   |   ├── serializer.py
|   |   └── summarizer.py
|   |
|   ├── admin.py
|   ├── apps.py
|   ├── models.py
|   ├── tests.py
|   ├── urls.py
|   └── views.py
│
├── docker-compose.yml
├── Dokcerfile
├── manage.py
├── README.md
└── requirements.txt
```
___
## Notes
* Document summaries are generated locally using `sumy` with the `TextRank` algorithm.
* Embeddings are generated locally using `sentence-transformers`.
* The LLM runs locally using the Hugging Face model (`google/flan-t5-base`) via `transformers pipeline`.
* The model is downloaded automatically the first time it is used.
* No external API calls are required.
* Internet connection is required only once for downloading the model.

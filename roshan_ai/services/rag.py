from transformers import pipeline
from langchain_huggingface import HuggingFacePipeline

pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_new_tokens=200,
    model_kwargs={
        "do_sample": True,
        "temperature": 0.3,
        "max_length": 512,
    },
)

llm = HuggingFacePipeline(pipeline=pipe)

def generate_answer(question_text: str, documents: str) -> str:
    context = documents
    prompt = f"""
Use the following document to answer the question.

Document:
{context}

Question:
{question_text}

Answer clearly and concisely.
"""
    return llm.invoke(prompt)

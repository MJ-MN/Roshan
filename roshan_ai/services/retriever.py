from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
FAISS_PATH = "data/faiss_index"

embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

vectorstore = FAISS.load_local(
    FAISS_PATH,
    embeddings,
    allow_dangerous_deserialization=True,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

def retrieve_documents(query):
    results = retriever.invoke(query)
    return [doc.page_content for doc in results]

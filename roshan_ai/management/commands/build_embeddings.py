from django.core.management.base import BaseCommand
from roshan_ai.models import RoshanDocument

from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document


class Command(BaseCommand):
    help = "Build FAISS embeddings index from RoshanDocument table"

    def handle(self, *args, **kwargs):
        self.stdout.write("Loading documents from database...")

        docs = RoshanDocument.objects.all()

        if not docs.exists():
            self.stdout.write(self.style.WARNING("No documents found."))
            return

        documents = []

        for doc in docs:
            combined_text = f"""
            Title: {doc.title}
            Content: {doc.content}
            """

            documents.append(
                Document(page_content=combined_text.strip())
            )

        self.stdout.write("Creating embeddings model...")

        embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        self.stdout.write("Generating FAISS index...")

        vectorstore = FAISS.from_documents(documents, embeddings)

        vectorstore.save_local("data/faiss_index")

        self.stdout.write(self.style.SUCCESS("Embeddings successfully built!"))

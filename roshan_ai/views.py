from rest_framework import generics, status
from rest_framework.response import Response

from .models import RoshanQuestion
from .services import serializers, retriever, rag


class QuestionCreateView(generics.CreateAPIView):
    queryset = RoshanQuestion.objects.all()
    serializer_class = serializers.QuestionSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        question_instance = serializer.save()
        question_text = question_instance.question_text
        related_documents = retriever.retrieve_documents(question_text)
        generated_answer = rag.generate_answer(
            question_text,
            related_documents[0]
        )
        question_instance.answer = generated_answer
        question_instance.save()
        return Response(
            {
                "id": question_instance.id,
                "question_text": question_text,
                "related_documents": related_documents,
                "answer": generated_answer,
            },
            status=status.HTTP_201_CREATED,
        )
from rest_framework import serializers
from ..models import RoshanQuestion, RoshanDocument
from . import matcher

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoshanQuestion
        fields = ['id', 'question_text', 'document']
        read_only_fields = ['document', 'answer']

    def create(self, validated_data):
        question_text = validated_data['question_text']

        documents = RoshanDocument.objects.all()
        doc_texts = [doc.content for doc in documents]

        if documents.exists():
            index, score = matcher.find_best_match(question_text, doc_texts)
            matched_document = documents[index]
            validated_data['document'] = matched_document

        return super().create(validated_data)

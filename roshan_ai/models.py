from django.db import models
from .services.summarizer import generate_summary

class RoshanTag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class RoshanDocument(models.Model):
    title = models.CharField(max_length=255)
    summary = models.TextField(blank=True, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    tag = models.ForeignKey(RoshanTag, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.content and not self.summary:
            self.summary = generate_summary(self.content, sentence_count=3)
        super().save(*args, **kwargs)

class RoshanQuestion(models.Model):
    question_text = models.TextField()
    document = models.ForeignKey(RoshanDocument, null=True, blank=True, on_delete=models.SET_NULL)
    answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question_text[:50]

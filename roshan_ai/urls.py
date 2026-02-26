from django.urls import path
from .views import QuestionCreateView

urlpatterns = [
    path('questions/', QuestionCreateView.as_view(), name='question-create'),
]

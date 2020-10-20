from django.urls import path
from .views import *

urlpatterns = [
    path('upload-question-bank', UploadQuestionBank.as_view()),
    path('upload-topic', UploadTopic.as_view()),
]
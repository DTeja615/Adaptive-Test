from django.urls import path
from .views import *

urlpatterns = [
    path('upload-student-details', UploadStudentDetails.as_view()),
    path('student-login', StudentLogin.as_view()),
    path('upload-student-answers', UploadStudentAnswers.as_view()),
    path('student-qna', StudendQnA.as_view()),
    path('previous-test-scores', PreviousTestScores.as_view()),
]
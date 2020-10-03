from django.urls import path
from .views import *

urlpatterns = [
    path('upload-faculty-details', UploadFacultyDetails.as_view()),
    path('faculty-login', FacultyLogin.as_view()),
    path('faculty-upload-question', FacultyUploadQuestion.as_view()),
    path('update-student-scores', UpdateStudentScores.as_view()),
    path('generate-mock-test', GenerateMockTest.as_view()),
    path('fetch-mock-test', FetchMockTest.as_view())
]

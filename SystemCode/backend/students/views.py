from rest_framework import views, status
from rest_framework.response import Response

from students.helpers.students import upload_student_details, student_login, upload_student_answers, previous_scores
from students.helpers.student_QnA import qna_response


class UploadStudentDetails(views.APIView):

    def post(self, request):
        upload_response = upload_student_details(request)
        return Response(data=upload_response, status=status.HTTP_200_OK)


class StudentLogin(views.APIView):

    def get(self, request):
        login_response = student_login(request)
        return Response(data=login_response, status=status.HTTP_200_OK)


class UploadStudentAnswers(views.APIView):

    def post(self, request):
        upload_response = upload_student_answers(request)
        return Response(data=upload_response, status=status.HTTP_200_OK)


class StudendQnA(views.APIView):

    def post(self, request):
        qna_resp = qna_response(request)
        return Response(data=qna_resp, status=status.HTTP_200_OK)


class PreviousTestScores(views.APIView):

    def get(self, request):
        response = previous_scores(request)
        return Response(data=response, status=status.HTTP_200_OK)

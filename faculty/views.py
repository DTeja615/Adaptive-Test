from rest_framework import views, status
from rest_framework.response import Response

from faculty.helpers.faculty import upload_faculty_details, faculty_login, faculty_upload_question, \
    update_student_scores


class UploadFacultyDetails(views.APIView):

    def post(self, request):
        upload_response = upload_faculty_details(request)
        return Response(data=upload_response, status=status.HTTP_200_OK)


class FacultyLogin(views.APIView):

    def get(self, request):
        login_response = faculty_login(request)
        return Response(data=login_response, status=status.HTTP_200_OK)


class FacultyUploadQuestion(views.APIView):

    def post(self, request):
        question_upload_response = faculty_upload_question(request)
        return Response(data=question_upload_response, status=status.HTTP_200_OK)


class UpdateStudentScores(views.APIView):

    def post(self, request):
        update_scores_response = update_student_scores(request)
        return Response(data=update_scores_response, status=status.HTTP_200_OK)



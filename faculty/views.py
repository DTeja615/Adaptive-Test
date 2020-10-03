from rest_framework import views, status
from rest_framework.response import Response

from faculty.helpers.faculty import upload_faculty_details, faculty_login, faculty_upload_question, \
    update_student_scores, fetch_mock_test
from faculty.MR import generate_mock_test


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


class GenerateMockTest(views.APIView):

    def get(self, request):
        generate_response = generate_mock_test(request)
        return Response(data=generate_response, status=status.HTTP_200_OK)


class FetchMockTest(views.APIView):

    def get(self, request):
        generate_response = fetch_mock_test(request)
        return Response(data=generate_response, status=status.HTTP_200_OK)


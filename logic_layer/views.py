from rest_framework import views, status
from rest_framework.response import Response

from logic_layer.helpers.database_upload import *


class UploadQuestionBank(views.APIView):

    def post(self, request):
        upload_response = upload_question_bank()
        return Response(data=upload_response, status=status.HTTP_200_OK)


class UploadTopic(views.APIView):

    def post(self, request):
        upload_response = upload_topic(request)
        return Response(data=upload_response, status=status.HTTP_200_OK)


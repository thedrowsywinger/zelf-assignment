from django.shortcuts import render
from django.http import JsonResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class ImageView(APIView):

    def get(self, request, *args, **kwargs):
        return Response({"message": "Success"}, status = status.HTTP_200_OK)
from django.shortcuts import render
from django.http import JsonResponse
from yaml import serialize

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from core.models import (
    Image as model
)

from core.serializers import (
    image_info_serializer
)

# Create your views here.


class ImageView(APIView):

    serializer_class = image_info_serializer

    def get(self, request, *args, **kwargs):

        result = model.objects.all()
        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

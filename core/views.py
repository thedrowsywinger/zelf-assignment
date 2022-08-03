from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from yaml import serialize

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import requests
from bs4 import BeautifulSoup
from random import choice

from core.models import (
    Image as model
)

from core.serializers import (
    image_info_serializer
)

from utils.constants import (
    user_agent_list
)

# Create your views here.


class ImageView(APIView):

    serializer_class = image_info_serializer

    def get(self, request, *args, **kwargs):

        result = model.objects.all()
        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ScrapeImagesView(APIView):

    def post(self, request, *args, **kwargs):
        result = requests.get(
            request.data['url'], headers={"User-Agent": choice(user_agent_list)})
        ebay_soup = BeautifulSoup(result.text, "html.parser")
        all_image_divs = ebay_soup.findAll('div', {"class": "b-tile__img"})
        image_srcs = [
            img.get('src')
            for i in all_image_divs
            for img in i.findChildren('img')
        ]

        title = 0
        for url in image_srcs:
            img_blob = requests.get(url, timeout=5).content
            with open("./" + settings.MEDIA_URL + str(title), 'wb') as img_file:
                img_file.write(img_blob)
            title += 1
        return Response({"message": "Success"}, status=status.HTTP_200_OK)

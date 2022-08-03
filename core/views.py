from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import requests
import uuid
from bs4 import BeautifulSoup
from random import choice

from core.models import (
    Image as model
)

from core.serializers import (
    image_info_serializer
)

from utils.constants import (
    get_extension_from_url,
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

        for url in image_srcs:
            img_blob = requests.get(url, timeout=5).content
            destination = settings.MEDIA_URL + str(uuid.uuid1())
            extension = get_extension_from_url(url)
            with open("." + destination + extension, 'wb') as img_file:
                img_file.write(img_blob)
                saving_image_instance = model(
                    image_path=destination + extension, meta_data={"original_url": url})
                saving_image_instance.save()

        return Response({"message": "Success"}, status=status.HTTP_200_OK)

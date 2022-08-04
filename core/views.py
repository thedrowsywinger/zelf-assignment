from utils.constants import (
    get_extension_from_url,
    get_file_path,
    user_agent_list
)
from core.serializers import (
    image_info_serializer
)
from core.models import (
    Image as model
)
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import requests
import uuid
import os
import pathlib
from bs4 import BeautifulSoup
from random import choice
from datetime import datetime
from PIL import Image
from zelf_scraper.settings import BASE_DIR


# Create your views here.


class ImageView(APIView):

    serializer_class = image_info_serializer

    def get(self, request, *args, **kwargs):

        print(request.data)

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
            image_from_bytes = Image.open(
                requests.get(url, timeout=5, stream=True).raw)
            file_path = get_file_path(url)
            if not file_path.startswith("/"):
                file_path = BASE_DIR.joinpath(file_path)
            else:
                file_path = BASE_DIR.joinpath(file_path[1:])
            print(file_path)
            image_from_bytes.save(file_path)
            try:
                saving_image_instance = model(
                    image_path=file_path,
                    original_url=request.data['url'],
                    meta_data={
                        "original_url": url,
                        "scrape_date": str(datetime.date(datetime.now())),
                        'height': image_from_bytes.height,
                        "width": image_from_bytes.width
                    })
                saving_image_instance.save()
            except:
                os.remove(file_path)

        return Response({"message": "Success"}, status=status.HTTP_200_OK)

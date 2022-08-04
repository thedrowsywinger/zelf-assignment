from utils.constants import (
    get_file_path,
    user_agent_list,
    api_response_messages
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
        try:
            if "id" in request.data:
                result = model.objects.get(id=request.data['id'])
                serializer = self.serializer_class(result)
                return Response({"message": api_response_messages["SUCCESS"], "data": serializer.data}, status=status.HTTP_200_OK)
            elif "original_url" in request.data:
                result = model.objects.filter(
                    original_url=request.data['original_url'])
                serializer = self.serializer_class(result, many=True)
                return Response({"message": api_response_messages["SUCCESS"], "count": len(result), "data": serializer.data}, status=status.HTTP_200_OK)
            else:
                result = model.objects.all()
                serializer = self.serializer_class(result, many=True)
                return Response({"message": api_response_messages["SUCCESS"], "count": len(result), "data": serializer.data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": api_response_messages['SYSTEM_ERROR'], "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ScrapeImagesView(APIView):

    def post(self, request, *args, **kwargs):
        try:
            result = requests.get(
                request.data['url'], headers={"User-Agent": choice(user_agent_list)})
            ebay_soup = BeautifulSoup(result.text, "html.parser")
            all_image_divs = ebay_soup.findAll(
                'div', {"class": "b-visualnav__img b-visualnav__img__default"})
            image_srcs = [
                img.get('src')
                for i in all_image_divs
                for img in i.findChildren('img')
            ]

            invalid_urls = []
            print(image_srcs)

            for url in image_srcs:
                try:
                    image_from_bytes = Image.open(
                        requests.get(url, timeout=5, stream=True).raw)
                    file_path, extension = get_file_path(url)
                    if extension != "gif":
                        if not file_path.startswith("/"):
                            file_path = BASE_DIR.joinpath(file_path)
                        else:
                            file_path = BASE_DIR.joinpath(file_path[1:])

                        image_from_bytes.save(file_path)

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
                        print("Saved")
                except Exception as e:
                    print(e)
                    invalid_urls.append(url)

            return Response({"message": api_response_messages['SUCCESS'], "Invalid URLs": invalid_urls}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": api_response_messages['SYSTEM_ERROR'], "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

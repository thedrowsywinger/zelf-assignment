from utils.constants import (
    get_file_path,
    resize_image,
    user_agent_list,
    api_response_messages,
    resized_image_status
)
from core.serializers import (
    image_info_serializer
)
from core.models import (
    Image as model
)
from django.shortcuts import render
from django.http import FileResponse, HttpResponse

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import requests
import base64
from wsgiref.util import FileWrapper
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
                image_path = result.image_path
                img = Image.open(image_path)
                resized_image = resized_image_status["NO"]
                if "size" in request.data:
                    width = result.meta_data['width']
                    height = result.meta_data['height']
                    if request.data['size'] == "small":
                        width, height, image_path = resize_image(img,
                                                                 "SMALL", result.image_path)
                        resized_image = resized_image_status["YES"]
                    elif request.data['size'] == "medium":
                        width, height, image_path = resize_image(img,
                                                                 "MEDIUM", result.image_path)
                        resized_image = resized_image_status["YES"]
                    elif request.data['size'] == "large":
                        width, height, image_path = resize_image(img,
                                                                 "LARGE", result.image_path)
                        resized_image = resized_image_status["YES"]
                    else:
                        resized_image = resized_image_status["NO"]

                if resized_image == resized_image_status["YES"]:
                    img.save(image_path)
                    serializer = self.serializer_class(result)
                    final_output = serializer.data
                    final_output['resized_image'] = {
                        "image_path": image_path,
                        "meta_data": {
                            "width": width,
                            "height": height
                        }
                    }

                    try:
                        with open(image_path, "rb") as image_file:
                            encoded_string = base64.b64encode(
                                image_file.read())
                            final_output['encoded_image'] = encoded_string
                            return Response({"message": api_response_messages["SUCCESS"], "data": final_output}, status=status.HTTP_200_OK)
                    except Exception as e:
                        return Response({"message": api_response_messages["IMAGE_ERROR"]}, status=status.HTTP_400_BAD_REQUEST)

                img.save(image_path)
                serializer = self.serializer_class(result)
                final_output = serializer.data
                try:
                    with open(image_path, "rb") as image_file:
                        encoded_string = base64.b64encode(
                            image_file.read())
                        final_output['encoded_image'] = encoded_string
                        return Response({"message": api_response_messages["SUCCESS"], "data": final_output}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"message": api_response_messages["IMAGE_ERROR"]}, status=status.HTTP_400_BAD_REQUEST)

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

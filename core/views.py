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

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

import requests
from bs4 import BeautifulSoup
from random import choice
from datetime import datetime
from PIL import Image
from zelf_scraper.settings import BASE_DIR


# Create your views here.


class ImageView(APIView):
    """
        This view will contain the querying part of the assessment. 
        The results are filtered based on either id or original url, or it returns all
        images. 
    """
    serializer_class = image_info_serializer

    def get(self, request, *args, **kwargs):
        try:
            if "id" in request.data:

                # Querying by id
                result = model.objects.get(id=request.data['id'])

                if "size" in request.data:
                    """
                        If size is in the POST request, that means the image 
                        needs to be resized. Therefore we need to get the
                        full path of the image, open it and resize it.
                    """
                    if not result.image_path.startswith("/"):
                        # My system has a media folder in the root, this is
                        # why I needed to handle this case
                        file_path = BASE_DIR.joinpath(result.image_path)
                    else:
                        file_path = BASE_DIR.joinpath(result.image_path[1:])
                    img = Image.open(file_path)
                    resized_image = resized_image_status["NO"]
                    width = result.meta_data['width']
                    height = result.meta_data['height']
                    if request.data['size'] == "small":
                        width, height, image_path, resized_server_file_path = resize_image(img,
                                                                                           "SMALL", file_path, result.image_path)
                        resized_image = resized_image_status["YES"]
                    elif request.data['size'] == "medium":
                        width, height, image_path, resized_server_file_path = resize_image(img,
                                                                                           "MEDIUM", file_path, result.image_path)
                        resized_image = resized_image_status["YES"]
                    elif request.data['size'] == "large":
                        width, height, image_path, resized_server_file_path = resize_image(img,
                                                                                           "LARGE", file_path, result.image_path)
                        resized_image = resized_image_status["YES"]
                    else:
                        resized_image = resized_image_status["NO"]

                if resized_image == resized_image_status["YES"]:
                    """
                        In this case the system will return the resized image
                        information alongside the original image information
                    """
                    img.save(image_path)
                    serializer = self.serializer_class(result)
                    final_output = serializer.data
                    final_output['resized_image'] = {
                        "image_path": resized_server_file_path,
                        "meta_data": {
                            "width": width,
                            "height": height
                        }
                    }

                    return Response({"message": api_response_messages["SUCCESS"], "data": final_output}, status=status.HTTP_200_OK)

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
        """
            Using choice from python random, to randomly choose a user agent for
            scraping, to avoid getting caught. 
        """
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

            for url in image_srcs:
                try:
                    image_from_bytes = Image.open(
                        requests.get(url, timeout=5, stream=True).raw)
                    server_file_path, extension = get_file_path(url)
                    if extension != "gif":
                        if not server_file_path.startswith("/"):
                            file_path = BASE_DIR.joinpath(server_file_path)
                        else:
                            file_path = BASE_DIR.joinpath(server_file_path[1:])

                        image_from_bytes.save(file_path)

                        saving_image_instance = model(
                            image_path=server_file_path,
                            original_url=request.data['url'],
                            meta_data={
                                "original_url": url,
                                "scrape_date": str(datetime.date(datetime.now())),
                                'height': image_from_bytes.height,
                                "width": image_from_bytes.width
                            })
                        saving_image_instance.save()
                except:
                    invalid_urls.append(url)

            return Response({"message": api_response_messages['SUCCESS'], "Invalid URLs": invalid_urls}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message": api_response_messages['SYSTEM_ERROR'], "details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

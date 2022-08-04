from rest_framework import serializers

from core.models import Image


class image_info_serializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = (
            'id',
            'image_path',
            "original_url",
            'meta_data'
        )

from django.urls import path
from core.views import (
    ImageView,
    ScrapeImagesView
)

urlpatterns = [
    path("image/", ImageView.as_view(), name="image_queries"),
    path("scrape-ebay/", ScrapeImagesView.as_view(), name="scrape_images")
]

from django.urls import path
from core.views import (
    ImageView,
    ScrapeImagesView
)

urlpatterns = [
    path("image/", ImageView.as_view(), name="test"),
    path("scrape-ebay/", ScrapeImagesView.as_view(), name="scrape_images")
]

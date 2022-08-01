from django.urls import path
from core.views import (
  ImageView
)

urlpatterns = [
  path("", ImageView.as_view(), name="test"),  
]
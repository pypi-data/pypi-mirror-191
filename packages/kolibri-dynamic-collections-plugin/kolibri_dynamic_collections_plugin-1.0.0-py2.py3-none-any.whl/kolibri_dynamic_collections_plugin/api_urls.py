from django.conf.urls import include
from django.conf.urls import url
from rest_framework import routers

from .api import AllContentNodeViewset

router = routers.DefaultRouter()

router.register(r"allcontentnode", AllContentNodeViewset, base_name="allcontentnode")

urlpatterns = [url(r"^", include(router.urls))]

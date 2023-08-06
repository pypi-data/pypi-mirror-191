from django.conf.urls import url

from . import views

urlpatterns = [url(r"^$", views.DynamicCollectionsRootView.as_view(), name="root")]

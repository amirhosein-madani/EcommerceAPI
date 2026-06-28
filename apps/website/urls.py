from django.urls import path
from . import views

app_name = "website"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("contact/", views.IndexView.as_view(), name="contact"),
    path("about/", views.IndexView.as_view(), name="about"),
]

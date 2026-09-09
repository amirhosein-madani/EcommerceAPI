from django.urls import path, include
from . import views

app_name = "website"

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("ticket/", views.TicketCreateView.as_view(), name="ticket"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("website/api/v1/", include("website.api.v1.urls")),
]

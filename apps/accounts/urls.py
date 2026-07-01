from django.urls import path, include
from .views import *

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", user_logout, name="logout"),
    # path("api/v1/", include("accounts.api.v1.urls")),
    # path('api/v2/' , include('djoser.urls')),
    # path('api/v2/' , include('djoser.urls.jwt')),
]

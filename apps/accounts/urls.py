from django.urls import path, include
from .views import *

urlpatterns = [
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("api/v1/", include("accounts.api.v1.urls")),
    path("sent-email/", sent_email, name="sent_email"),
    path("test-cache/", test_cache, name="test_cacging"),
    path("cache/", test_cahing, name="test_cacging"),
    # path('api/v2/' , include('djoser.urls')),
    # path('api/v2/' , include('djoser.urls.jwt')),
]

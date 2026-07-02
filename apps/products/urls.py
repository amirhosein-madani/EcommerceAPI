from django.urls import path

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
]

from django.urls import path
from .views import (
    NewsletterListApiView,
    NewsletterRetrieveDestroyAPIView,
    TicketListCreateAPIView,
    TicketRetrieveDestroyAPIView,
    TicketMessageListCreateAPIView,
    TicketMessageRetrieveAPIView,
    WishlistRetrieveUpdateAPIView,
)

urlpatterns = [
    path("newsletter-list/", NewsletterListApiView.as_view(), name="newsletter-list"),
    path(
        "newsletter-detail/<int:pk>/",
        NewsletterRetrieveDestroyAPIView.as_view(),
        name="newsletter-detail",
    ),
    path("ticket/", TicketListCreateAPIView.as_view(), name="ticket-list"),
    path(
        "ticket/<int:pk>/", TicketRetrieveDestroyAPIView.as_view(), name="ticket-detail"
    ),
    path("message/", TicketMessageListCreateAPIView.as_view(), name="message-list"),
    path(
        "message/<int:pk>/",
        TicketMessageRetrieveAPIView.as_view(),
        name="message-detail",
    ),
    path("wishlist/", WishlistRetrieveUpdateAPIView.as_view(), name="wishlist"),
]

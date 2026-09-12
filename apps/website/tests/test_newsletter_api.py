import pytest
from django.urls import reverse
from website.models import TicketMessage


@pytest.mark.django_db
class TestTicketMessageApi:

    def test_ticket_message_list_with_anonymous_user(self, api_client):
        url = reverse("website:message-list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_ticket_message_list_with_normal_user(self, api_client, normal_user):
        api_client.force_authenticate(normal_user)
        url = reverse("website:message-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_ticket_message_with_normal_user_response_201_status(
        self, api_client, normal_user, comon_ticket
    ):
        api_client.force_authenticate(normal_user)
        url = reverse("website:message-list")
        data = {"ticket": comon_ticket.pk, "message": "fjwoifjwioefj"}
        response = api_client.post(url, data)
        assert TicketMessage.objects.filter(
            ticket=comon_ticket.pk, message=data["message"]
        ).exists()
        assert response.status_code == 201

    def test_create_ticket_message_with_normal_user_response_400_status(
        self, api_client, normal_user, comon_ticket
    ):
        api_client.force_authenticate(normal_user)
        url = reverse("website:message-list")
        data = {}
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_ticket_message_detail_with_anonymous_user_response_401_status(
        self, api_client, normal_user, comon_ticket_message
    ):
        url = reverse("website:message-detail", kwargs={"pk": comon_ticket_message.pk})
        response = api_client.get(url)
        assert response.status_code == 401

    def test_ticket_message_detail_with_normal_user_response_200_status(
        self, api_client, normal_user, comon_ticket_message
    ):
        api_client.force_authenticate(normal_user)
        url = reverse("website:message-detail", kwargs={"pk": comon_ticket_message.pk})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_another_user_ticket_message_detail_response_404_status(
        self, api_client, another_user, comon_ticket_message
    ):
        api_client.force_authenticate(another_user)
        url = reverse("website:message-detail", kwargs={"pk": comon_ticket_message.pk})
        response = api_client.get(url)
        assert response.status_code == 404

import pytest
from django.urls import reverse
from website.models import Ticket


@pytest.mark.django_db
class TestTicketApi:

    def test_ticket_list_with_anonymous_user(self, api_client):
        url = reverse("website:ticket-list")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_ticket_list_with_normal_user(self, api_client, normal_user):
        api_client.force_authenticate(normal_user)
        url = reverse("website:ticket-list")
        response = api_client.get(url)
        assert response.status_code == 200

    def test_create_ticket_with_normal_user_response_201_status(
        self, api_client, normal_user
    ):
        api_client.force_authenticate(normal_user)
        url = reverse("website:ticket-list")
        data = {"subject": "oweiji"}
        response = api_client.post(url, data)
        assert Ticket.objects.filter(user=normal_user, subject=data["subject"]).exists()
        assert response.status_code == 201

    def test_create_ticket_with_normal_user_response_400_status(
        self, api_client, normal_user
    ):
        api_client.force_authenticate(normal_user)
        url = reverse("website:ticket-list")
        data = {}
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_create_ticket_with_anonymous_user_response_401_status(
        self, api_client, normal_user
    ):
        url = reverse("website:ticket-list")
        data = {"subject": "oweiji"}
        response = api_client.post(url, data)
        assert response.status_code == 401

    def test_ticket_detail_with_anonymous_user_response_401_status(
        self, api_client, normal_user, comon_ticket
    ):
        url = reverse("website:ticket-detail", kwargs={"pk": comon_ticket.pk})
        response = api_client.get(url)
        assert response.status_code == 401

    def test_ticket_detail_with_normal_user_response_200_status(
        self, api_client, comon_ticket, normal_user
    ):
        api_client.force_authenticate(normal_user)
        url = reverse("website:ticket-detail", kwargs={"pk": comon_ticket.pk})
        response = api_client.get(url)
        assert response.status_code == 200

    def test_another_user_ticket_detail_response_404_status(
        self, api_client, another_user, comon_ticket
    ):
        api_client.force_authenticate(another_user)
        url = reverse("website:ticket-detail", kwargs={"pk": comon_ticket.pk})
        response = api_client.get(url)
        assert response.status_code == 404

    def test_delete_ticket_with_anonymous_user_response_401_status(
        self, api_client, normal_user, comon_ticket
    ):
        url = reverse("website:ticket-detail", kwargs={"pk": comon_ticket.pk})
        response = api_client.delete(url)
        assert response.status_code == 401

    def test_delete_ticket_with_normal_user_response_204_status(
        self, api_client, comon_ticket, normal_user
    ):
        api_client.force_authenticate(normal_user)
        url = reverse("website:ticket-detail", kwargs={"pk": comon_ticket.pk})
        response = api_client.delete(url)
        assert not Ticket.objects.filter(user=normal_user, pk=comon_ticket.pk).exists()
        assert response.status_code == 204

    def test_delete_another_user_ticket_response_404_status(
        self, api_client, another_user, comon_ticket
    ):
        api_client.force_authenticate(another_user)
        url = reverse("website:ticket-detail", kwargs={"pk": comon_ticket.pk})
        response = api_client.delete(url)
        assert response.status_code == 404

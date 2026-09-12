import pytest
from rest_framework.test import APIClient
from accounts.models import User
from website.models import Ticket, TicketMessage, Wishlist
from products.models import ProductStatusType, Product


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def admin_user():
    user = User.objects.create_superuser(
        username="amir",
        password="amirmad2007",
        email="amirmadani901@gmail.com",
        national_code="6300110117",
    )
    return user


@pytest.fixture
def normal_user():
    user = User.objects.create_user(
        username="normal",
        password="amirmad2007",
        email="example@gmail.com",
        national_code="0250704961",
    )
    return user


@pytest.fixture
def another_user():
    user = User.objects.create_user(
        username="worqkjg0wrjg0wrjgiorw",
        password="amirmad2007",
        email="examfefefefefefple@gmail.com",
        national_code="2583094327",
    )
    return user


@pytest.fixture
def comon_ticket(normal_user):
    ticket = Ticket.objects.create(user=normal_user, subject="efvnoiwnefiow")
    return ticket


@pytest.fixture
def another_user_ticket(another_user):
    ticket = Ticket.objects.create(user=another_user, subject="efvnoiwnefiow")
    return ticket


@pytest.fixture
def comon_ticket_message(normal_user, comon_ticket):
    ticket = TicketMessage.objects.create(
        ticket=comon_ticket,
        sender=normal_user,
        message="wnvowngoiernfgioerhuwqioerfbhwurif",
    )
    return ticket


@pytest.fixture
def common_product():
    product = Product.objects.create(
        title="test",
        description="mwomweokfmwoiefwoief",
        price=100000000,
        status=ProductStatusType.PUBLISH,
    )
    return product


@pytest.fixture
def common_wishlist(db, normal_user, common_product):
    wishlist, _ = Wishlist.objects.get_or_create(user=normal_user)
    wishlist.products.add(common_product)
    return wishlist


@pytest.fixture
def admin_wishlist(db, admin_user):
    wishlist, _ = Wishlist.objects.get_or_create(user=admin_user)
    return wishlist

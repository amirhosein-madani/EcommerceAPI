from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from order.models import Order, OrderStatusType


@shared_task
def expired_orders():
    now = timezone.now()

    orders = Order.objects.filter(
        status=OrderStatusType.PENDING, created_at__lte=now - timedelta(minutes=15)
    )

    orders.update(status=OrderStatusType.CANCELED)

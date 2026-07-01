from celery import shared_task
from time import sleep
from templated_email import send_templated_mail


@shared_task
def send_reset_password_email(email, reset_link, username):
    send_templated_mail(
        template_name="reset-password",
        from_email="noreply@example.com",
        recipient_list=[email],
        context={
            "username": username,
            "reset_link": reset_link,
            "site_name": "My Shop",
        },
    )

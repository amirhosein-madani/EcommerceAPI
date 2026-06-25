from celery import shared_task
from time import sleep


@shared_task
def send_email():
    sleep(3)
    return "📧 Email sent successfully"


@shared_task
def cleanup_old_task_results():

    from django_celery_results.models import TaskResult

    deleted_count, _ = TaskResult.objects.filter(status="SUCCESS").delete()

    return f"{deleted_count} successful tasks cleaned up"

from celery import shared_task
from django.core.mail import send_mail
from config import settings
from materials.models import Subscription


@shared_task
def start_mailshot(course):
    """Отправляет сообщения пользователям с подпиской об обновлениях материалов курса."""

    course_updates = Subscription.objects.filter(course=course.id)
    for single_update in course_updates:
        send_mail(
            subject="Материалы курса обновились!",
            message=f"Произошло обновление материалов курса - {single_update.course.title}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[single_update.user.email],
        )
    print("Сообщение отправлено")

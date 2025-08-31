from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Task
from django.conf import settings
import threading

# для безопасного хранения данных между сигналами в одном потоке
_thread_locals = threading.local()

@receiver(pre_save, sender=Task)
def store_old_status(sender, instance, **kwargs):
    """
    Сохраняем старый статус задачи перед её сохранением
    """
    if instance.pk:
        # Если объект существует в базе, получаем его старый статус
        try:
            old_instance = Task.objects.get(pk=instance.pk)
            _thread_locals.old_status = old_instance.status
        except Task.DoesNotExist:
            _thread_locals.old_status = None
    else:
        _thread_locals.old_status = None


@receiver(post_save, sender=Task)
def task_status_changed(sender, instance, created, **kwargs):
    """
    Отправляет email-уведомление, если статус задачи был изменен
    """
    # Если объект только что создан, не отправляем уведомление
    if created:
        return

    # Получаем старый статус, который мы сохранили в pre_save
    old_status = getattr(_thread_locals, 'old_status', None)

    # Проверяем, изменился ли статус
    if old_status != instance.status:
        # Проверяем, что задача принадлежит кому-то
        if instance.owner and instance.owner.email:
            subject = f"The status of your task '{instance.title}' has changed"
            message = f"Hello, {instance.owner.username}!\n\n" \
                      f"The status of your task '{instance.title}' has been updated.\n" \
                      f"Previous status: {old_status}\n" \
                      f"New status: {instance.status}\n\n" \
                      f"Best regards,\nThe Task Manager Team"

            # Отправляем email-уведомление
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [instance.owner.email],
                fail_silently=False,
            )
            print(f"Email notification has been sent to user {instance.owner.username}")
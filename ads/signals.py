from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Ad


@receiver(post_save, sender=Ad)
def ad_created_or_updated(sender, instance, created, **kwargs):
    if created:
        print(f"🔔 Новое объявление создано: '{instance.title}' от {instance.user}")
        # например: отправить email/уведомление
    else:
        print(f"✏️ Объявление обновлено: '{instance.title}'")


@receiver(post_delete, sender=Ad)
def ad_deleted(sender, instance, **kwargs):
    print(f"🗑️ Объявление удалено: '{instance.title}' от {instance.user}")
    # например: удалить связанные файлы, логировать и т.п.

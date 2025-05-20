from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.db.models import Q, F, Index


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
        

class Ad(models.Model):
    CONDITION_CHOICES = [
        ("new", "Новый"),
        ("used", "Б/у"),
    ]

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ads")
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="ads_images/", blank=True, null=True)

    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, blank=True, related_name="ads")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"
        ordering = ['-created_at']  # последние объявления первыми
        indexes = [
            Index(fields=['user', 'created_at']),
        ]
        constraints = [
            models.CheckConstraint(
                check=~Q(title=""),  # title не должен быть пустым
                name="check_ad_title_not_empty"
            ),
            models.UniqueConstraint(fields=['user', 'title'], name='unique_user_title')
        ]

    @property
    def is_new(self):
        return self.condition == "new"



class ExchangeProposal(models.Model):
    STATUS_CHOICES = [
        ("pending", "Ожидает"),
        ("accepted", "Принята"),
        ("rejected", "Отклонена"),
    ]

    id = models.BigAutoField(primary_key=True)
    ad_sender = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="sent_proposals")
    ad_receiver = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name="received_proposals")
    comment = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Предложение обмена от '{self.ad_sender}' к '{self.ad_receiver}' [{self.get_status_display()}]"

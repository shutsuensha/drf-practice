# Register your models here.
from django.contrib import admin
from .models import Category, Tag, Ad, ExchangeProposal


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title")
    search_fields = ("title",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "user", "category", "condition", "created_at")
    list_filter = ("condition", "category", "created_at")
    search_fields = ("title", "description", "user__username")
    autocomplete_fields = ("user", "category", "tags")
    filter_horizontal = ("tags",)


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(admin.ModelAdmin):
    list_display = ("id", "ad_sender", "ad_receiver", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = (
        "ad_sender__title",
        "ad_receiver__title",
        "comment",
    )

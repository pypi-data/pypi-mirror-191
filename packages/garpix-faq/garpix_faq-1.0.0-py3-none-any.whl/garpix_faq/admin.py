from django.contrib import admin

from .models import FaqInfo


@admin.register(FaqInfo)
class FaqInfoAdmin(admin.ModelAdmin):
    list_display = ['title', 'number', 'created_at']
    list_editable = ['number', ]

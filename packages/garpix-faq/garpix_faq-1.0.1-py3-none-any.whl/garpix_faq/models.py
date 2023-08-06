from ckeditor.fields import RichTextField
from django.db import models
from django.utils.translation import gettext_lazy as _


class FaqInfo(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Вопрос'))
    answer = RichTextField(verbose_name=_('Ответ'))
    number = models.IntegerField(default=0, verbose_name=_('Флаг для сортировки'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'
        ordering = ['number']

    def __str__(self):
        return self.title

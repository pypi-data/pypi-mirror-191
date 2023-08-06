from django.conf import settings
from django.urls import path, include
from rest_framework import routers
from . import views

app_name = 'garpix_faq'

API_URL = getattr(settings, 'API_URL', 'api')

router = routers.DefaultRouter()
router.register(r'faq', views.FaqInfoViewSet, basename='faq')

urlpatterns = [
    path(f'{API_URL}/', include(router.urls)),
]

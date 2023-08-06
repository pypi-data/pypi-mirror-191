from rest_framework import mixins
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import GenericViewSet

from .models import FaqInfo
from .serializers import FaqInfoSerializer


class FaqInfoViewSet(mixins.ListModelMixin, GenericViewSet):
    queryset = FaqInfo.objects.order_by('number')
    serializer_class = FaqInfoSerializer
    filter_backends = (OrderingFilter, SearchFilter)
    search_fields = ['title', 'answer']

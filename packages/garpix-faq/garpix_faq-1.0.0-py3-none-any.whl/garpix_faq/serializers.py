from rest_framework.serializers import ModelSerializer

from .models import FaqInfo


class FaqInfoSerializer(ModelSerializer):
    class Meta:
        model = FaqInfo
        fields = '__all__'

from rest_framework import serializers
from .models import Contacto

class ConsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contacto
        fields = '__all__'

class VinoExternoSerializer(serializers.Serializer):
    wine = serializers.CharField(max_length=200)
    winery = serializers.CharField(max_length=200)
    rating = serializers.DictField()
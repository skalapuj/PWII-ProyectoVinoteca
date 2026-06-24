from rest_framework import viewsets
from .models import Contacto
from .serializers import ConsultaSerializer

class ConsultaViewSet(viewsets.ModelViewSet):
    queryset = Contacto.objects.all()
    serializer_class = ConsultaSerializer
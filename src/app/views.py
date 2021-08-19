from rest_framework import generics
from .models import Scheduling
from .serializers import SchedulingSerializer
from django_filters import rest_framework as filters


# Create your views here.
class SchedulingList(generics.RetrieveAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer


class SchedulingCreate(generics.CreateAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = '__all__'

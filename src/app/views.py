from rest_framework import generics
from .models import Scheduling
from .serializers import SchedulingSerializer
from django_filters import rest_framework as filters


# Create your views here.
class SchedulingSearchId(generics.RetrieveAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer


class SchedulingSearchList(generics.ListAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('sender', 'date_send', 'receiver', 'message', 'date_entry', 'status')


class SchedulingCreate(generics.CreateAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer


class SchedulingDelete(generics.DestroyAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer

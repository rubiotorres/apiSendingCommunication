
from rest_framework import generics
from .models import Scheduling
from .serializers import SchedulingSerializer
from django_filters import rest_framework as filters

# Create your views here.
class SchedulingList(generics.ListCreateAPIView):

    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer
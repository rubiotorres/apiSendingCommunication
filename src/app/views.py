from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.response import Response

from .models import Scheduling
from .serializers import SchedulingSerializer


# Create your views here.
class SchedulingSearchId(generics.RetrieveAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return Response({
            'status': 200,
            'data': response.data
        })


class SchedulingSearchList(generics.ListAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('sender', 'date_send', 'receiver', 'message', 'date_entry', 'status')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        if response.data:
            return Response({
                'status': 200,
                'data': response.data
            })
        else:
            return Response({
                'status': 404,
                'data': response.data
            })


class SchedulingCreate(generics.CreateAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response({
            'status': 200,
            'message': 'Your message has been scheduled.',
            'data': response.data
        })


class SchedulingDelete(generics.DestroyAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer

    def destroy(self, request, *args, **kwargs):
        return Response({
            'status': 200,
            'message': 'Your message has been canceled.'
        })

from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Scheduling
from .serializers import SchedulingSerializer


# Create your views here.
class SchedulingSearchId(generics.RetrieveAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return Response({
            'status': status.HTTP_200_OK,
            'data': response.data
        })


class SchedulingSearchList(generics.ListAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filter_fields = ('sender', 'date_send', 'receiver', 'message', 'date_entry', 'status')
    permission_classes = (IsAuthenticated, )

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({
            'status': status.HTTP_200_OK,
            'data': response.data
        })


class SchedulingCreate(generics.CreateAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Your message has been scheduled.',
            'data': response.data
        })


class SchedulingDelete(generics.DestroyAPIView):
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer
    permission_classes = (IsAuthenticated, )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Your message has been deleted.'})

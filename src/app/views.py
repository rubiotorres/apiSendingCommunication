from django_filters import rest_framework as filters
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Scheduling
from .serializers import SchedulingSerializer

# A `view` receives an HTTP request through an endpoint and returns a response from the web.
# Create your views here.

class SchedulingSearchId(generics.RetrieveAPIView):
    # Search for a scheduled message by ID.
    # GET: /scheduling/status/id/<id>
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        return Response({
            'status': response.data['status']
        })


class SchedulingSearchList(generics.ListAPIView):
    # Search list of scheduled messages
    # This endpoint supports filters 
    # by fields via the url as per the documentation
    # GET /scheduling/search/ 
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
    # Receive the message schedule
    # POST: /scheduling/create/
    # Receive a JSON in the message body
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
    # DELETE a scheduled message by id
    # DELETE /scheduling/delete/
    queryset = Scheduling.objects.all()
    serializer_class = SchedulingSerializer
    permission_classes = (IsAuthenticated, )

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Your message has been deleted.'})

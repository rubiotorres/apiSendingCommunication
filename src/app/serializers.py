from rest_framework import serializers
from .models import Scheduling
from datetime import datetime


class SchedulingSerializer(serializers.ModelSerializer):
    class Meta:

        model = Scheduling
        fields = ('id','sender','date_send','receiver','message')
        read_only_fields = ('date_entry', 'status')
        fields = '__all__'
from rest_framework import serializers

from .models import Scheduling


# The `serializers` allow you to interpret input in JSON, XML or other complex types.
class SchedulingSerializer(serializers.ModelSerializer):
    # fields list: List of fields required when creating an object
    # read_only_fields list: List of required elements read-only
    class Meta:
        model = Scheduling
        fields = '__all__'
        read_only_fields = ('date_entry', 'status')

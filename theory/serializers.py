from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import AlgorithmTheory

class ProcessSerializer(serializers.Serializer):
    pid = serializers.CharField()
    arrival = serializers.IntegerField(min_value=0, required=False)
    burst = serializers.IntegerField(min_value=1, required=False)
    priority = serializers.IntegerField(min_value=1, required=False)

class SchedulingSimulationSerializer(serializers.Serializer):
    # For CPU scheduling
    processes = ProcessSerializer(many=True, required=False)
    quantum = serializers.IntegerField(min_value=1, required=False)

    # For memory allocation
    blocks = serializers.ListField(child=serializers.IntegerField(min_value=1), required=False)

    # For page replacement
    pages = serializers.ListField(child=serializers.IntegerField(min_value=0), required=False)

    # For banker’s algorithm
    alloc = serializers.ListField(
        child=serializers.ListField(child=serializers.IntegerField(min_value=0)), required=False
    )
    max_req = serializers.ListField(
        child=serializers.ListField(child=serializers.IntegerField(min_value=0)), required=False
    )
    avail = serializers.ListField(child=serializers.IntegerField(min_value=0), required=False)

class AlgorithmTheorySerializer(DocumentSerializer):
    class Meta:
        model = AlgorithmTheory
        fields = '__all__'


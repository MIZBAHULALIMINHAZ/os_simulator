from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import AlgorithmTheory
# theory/serializers.py
# theory/serializers.py
from rest_framework import serializers

class ProcessSerializer(serializers.Serializer):
    pid = serializers.CharField()
    arrival = serializers.IntegerField(min_value=0)
    burst = serializers.IntegerField(min_value=1)
    priority = serializers.IntegerField(min_value=1, required=False)  # for Priority scheduling

class SchedulingSimulationSerializer(serializers.Serializer):
    processes = ProcessSerializer(many=True)
    quantum = serializers.IntegerField(min_value=1, required=False)  # for Round Robin


class AlgorithmTheorySerializer(DocumentSerializer):
    class Meta:
        model = AlgorithmTheory
        fields = '__all__'


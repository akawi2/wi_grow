from rest_framework import serializers
from .models import EnvironmentalMonitoring, Incident

class EnvironmentalMonitoringSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalMonitoring
        fields = '__all__'
        
class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = '__all__'
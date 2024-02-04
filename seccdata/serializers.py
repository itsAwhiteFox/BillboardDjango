from rest_framework import serializers
from .models import SeccData

class SECCSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeccData
        fields = '__all__'

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeccData
        fields = ['State', 'District', 'SubDistrict']

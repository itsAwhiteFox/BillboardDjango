from rest_framework import serializers
from .models import Campaigns
from sites.models import Site

class CampaignsSerializer(serializers.ModelSerializer):
    assignedSites = serializers.PrimaryKeyRelatedField(queryset=Site.objects.all(), many=True)

    class Meta:
        model = Campaigns
        fields = ['code', 'campaignName', 'created', 'assigned_customer', 'startDate', 'endDate', 'assignedSites']

from rest_framework import serializers
from .models import Site, Booking, SiteImages, SitePricing, SiteGoogleStats

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


class SitePricingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SitePricing
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'

class PPTSerializer(serializers.Serializer):
    ppt_file = serializers.FileField()

class ImagePathsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteImages
        fields = '__all__'

class GooglePlacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteGoogleStats
        fields = '__all__'

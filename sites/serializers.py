from rest_framework import serializers
from .models import Site, Booking, SiteImages

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    site = SiteSerializer()

    class Meta:
        model = Booking
        fields = '__all__'

class PPTSerializer(serializers.Serializer):
    ppt_file = serializers.FileField()

class ImagePathsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SiteImages
        fields = ['siteName', 'path']

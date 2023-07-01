import os
import uuid
from pptx import Presentation
from PIL import Image
from rest_framework.parsers import MultiPartParser
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pptx.enum.shapes import MSO_SHAPE_TYPE

from .models import Site, Booking, SiteImages
from .serializers import SiteSerializer, BookingSerializer, ImagePathsSerializer
from sites.tasks import process_data
import googlemaps

class SitesAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            site = Site.objects.get(pk=pk)
            serializer = SiteSerializer(site)
            return Response(serializer.data)
        
        site = Site.objects.all()
        serializer = SiteSerializer(site, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        data["siteTag"] = str(uuid.uuid4())
        serializer = SiteSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            process_data(data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SitesSearchView(APIView):
    def get(self, request):

        searchText = request.query_params.get('searchText')
        print("searchText", searchText)
        queryset = Site.objects.filter(
            Q(location__icontains=searchText) | Q(priorityArea__icontains=searchText) | Q(town__icontains=searchText)
        )
        serializer = SiteSerializer(queryset, many=True)

        return Response(serializer.data)
        
class BookingAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            booking = Booking.objects.get(pk=pk)
            serializer = BookingSerializer(booking)
            return Response(serializer.data)
        
        booking = Booking.objects.all()
        serializer = BookingSerializer(booking, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PPTUploadView(APIView):    
    parser_classes = [MultiPartParser]

    def post(self, request, format=None):
        ppt_file = request.FILES.get('ppt_file')
        if ppt_file is None:
            return Response({'error': 'No file uploaded'}, status=400)

        images_folder = os.path.join(settings.STATIC_ROOT, 'ppt_images')
        
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        presentation = Presentation(ppt_file)
        sitesUploaded = []
        slideNotUploaded = []
        index = 0
        for slide in presentation.slides:
            image = None
            text = None
            for shape in slide.shapes:
                if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                    image = shape.image
                
                if shape.has_text_frame:
                    if not text:
                        text = shape.text_frame.text.strip()
                    
            if image and text:
                try:
                    image_filename = os.path.join(images_folder, text+".jpeg")
                    image_bytes = image.blob
                    with open(image_filename, 'wb') as f:
                        f.write(image_bytes)
                    sitesUploaded.append({"siteName": text, "path": image_filename})
                except:
                    slideNotUploaded.append("Slide " + str(index) + " not uploaded due to name error")

            elif not image or not text:
                if not image:
                    slideNotUploaded.append("Slide " + str(index) + " not uploaded as image not there")
                if not text: 
                    slideNotUploaded.append("Slide " + str(index) + " not uploaded as text not there")
            
            index = index+1

        serializer = ImagePathsSerializer(data=sitesUploaded, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'images': sitesUploaded, 'notUploaded':slideNotUploaded})
        else:
            return Response({'error': 'some error happened'}, status=status.HTTP_400_BAD_REQUEST)


class ImageView(APIView):
    def get(self, request, format=None):
        images_folder = os.path.join(settings.STATIC_ROOT, 'ppt_images')
        if not os.path.exists(images_folder):
            return Response({'error': 'Images folder not found'}, status=404)

        image_data = []
        for filename in os.listdir(images_folder):
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                image_path = os.path.join(images_folder, filename)
                with open(image_path, 'rb') as f:
                    image_data.append(f.read())

        response = HttpResponse(content_type='image/jpeg')
        for data in image_data:
            response.write(data)

        return response



class GetPlacesGoogle(APIView):
    def get(self, request):
        location = request.GET.get('location')
        radius = request.GET.get('radius', 2000)
        keyword = request.GET.get('keyword', 'bank')

        gmaps = googlemaps.Client("AIzaSyAmnjoE7eFekledKAqF8ctrMoNBk3w0Xm8")
        places = gmaps.places_nearby(
            location=location,
            radius=radius,
            keyword=keyword
        )

        results = []
        for place in places['results']:
            print(place)
            result = {
                'name': place['name'],
                'address': place['vicinity'],
                'status':place['business_status'],
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng'],
                'place_id': place['place_id']
            }
            results.append(result)

        return Response(results)
    
class PlaceDetailAPI(APIView):
    def get(self, request):
        place_id = request.GET.get('place_id')
        gmaps = googlemaps.Client("AIzaSyAmnjoE7eFekledKAqF8ctrMoNBk3w0Xm8")

        place_details = gmaps.place(place_id=place_id)
        return Response(place_details['result'])
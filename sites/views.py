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

from .models import Site, Booking, SiteImages, SitePricing
from .serializers import SiteSerializer, BookingSerializer, ImagePathsSerializer, SitePricingSerializer
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


class SitePricingAPIView(APIView):
    def get(self, request, pk=None):
        if pk is not None:
            pricing = SitePricing.objects.get(pk=pk)
            serializer = SitePricingSerializer(pricing)
            return Response(serializer.data)
        
        pricing = SitePricing.objects.all()
        serializer = SitePricingSerializer(pricing, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        data = request.data
        serializer = SitePricingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PriceFetchSite(APIView):
    def get(self, request):
        searchText = request.query_params.get('siteTag')
        pricing = SitePricing.objects.filter(site_id=searchText)
        
        serializer = SitePricingSerializer(pricing, many=True)
        
        return Response(serializer.data)


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
    parser_classes = [MultiPartParser]

    def get(self, request, pk=None):
        
        if pk is not None:
            image = SiteImages.objects.get(pk=pk)
            serializer = ImagePathsSerializer(image)
            image_data = None
            print(serializer.data["path"])
            with open(serializer.data["path"], 'rb') as f:
                image_data = f.read()
            response = HttpResponse(content_type='image/jpeg')
            response.write(image_data)
            print("response",response)
            return response
    
        images = SiteImages.objects.all()
        serializer = ImagePathsSerializer(images, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, format=None):
        image_file = request.FILES.get('image')
        siteName = request.data.get('siteName')
        siteTag = request.data.get('siteTag')
        
        if image_file is None:
            return Response({'error': 'No file uploaded'}, status=400)

        images_folder = os.path.join(settings.STATIC_ROOT, 'ppt_images')
        
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)

        image_filename = os.path.join(images_folder, siteName + ".jpeg")
        image_bytes = image_file.read()
        with open(image_filename, 'wb') as f:
            f.write(image_bytes)
                    
        serializer = ImagePathsSerializer(data={"siteName": siteName, "path": image_filename, "site":siteTag})
        if serializer.is_valid():
            serializer.save()
            return Response({"siteName": siteName, "path": image_filename, "site":siteTag})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ImagesSearchView(APIView):
    def get(self, request):
        searchText = request.query_params.get('searchText')
        queryset = SiteImages.objects.filter(
            Q(siteName__icontains=searchText)
        )

        serializer = ImagePathsSerializer(queryset, many=True)
        
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

class BookingByCustomer(APIView):
    def get(self, request):
        searchText = request.query_params.get('customerID')
        queryset = Booking.objects.get(assigned_to=searchText)
        serializer = BookingSerializer(queryset, many=True)
        return Response(serializer.data)

class ImagesFetchSiteTagView(APIView):
    def get(self, request):
        searchText = request.query_params.get('siteTag')

        queryset = SiteImages.objects.get(site_id=searchText)
        
        serializer = ImagePathsSerializer(queryset)
        print(serializer.data)
        image_data = None    
        with open(serializer.data["path"], 'rb') as f:
            image_data = f.read()
        response = HttpResponse(content_type='image/jpeg')
        response.write(image_data)
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
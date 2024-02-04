import os
import uuid
import math
from datetime import datetime
import time
from pptx import Presentation
from django.conf import settings
from django.db.models import Q
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser
from pptx.enum.shapes import MSO_SHAPE_TYPE
from django.core.exceptions import ObjectDoesNotExist

from .models import Site, Booking, SiteImages, SitePricing, GoogleStats, IndiaGrid, StateEntities
from .serializers import SiteSerializer, BookingSerializer, ImagePathsSerializer, SitePricingSerializer, GooglePlacesSerializer, IndiaGridSerializer, StateEntitiesSerializer

import googlemaps




# class GooglePlacesAPIView(APIView):
#     def get(self, request):
#         searchText = request.query_params.get('siteTag')
#         sitesData = SiteGoogleStats.objects.filter(site_id=searchText)
#         serializer = GooglePlacesSerializer(sitesData, many=True)        
#         return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_india_grid(request):
    grid = IndiaGrid.objects.all()
    serializer = IndiaGridSerializer(grid, many=True)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_india_grid(request):
    data = request.data
    serializer = IndiaGridSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        # process_data(data)
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_state_entities(request):
    entity = StateEntities.objects.all()
    serializer = StateEntitiesSerializer(entity, many=True)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_state_entities(request):
    data = request.data
    serializer = StateEntitiesSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        # process_data(data)
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_site_detail(request, pk):
    site = Site.objects.get(pk=pk)
    serializer = SiteSerializer(site)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)




@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_sites_list(request):
    site = Site.objects.all()
    serializer = SiteSerializer(site, many=True)
    print(serializer)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_new_site(request):
    data = request.data
    data["siteTag"] = str(uuid.uuid4())
    if float(data["site_lat"]) < 8.4 or float(data["site_lat"]) > 37.6 or float(data["site_long"]) > 97.3 or float(data["site_long"]) < 68.7:
        Response({"success":False, "data":"Latitude and/or Longitude out of bounds"}, status=status.HTTP_400_BAD_REQUEST)
    data["grid"] = str(math.ceil((float(data["site_lat"])-8.4)/.05))+"_"+str(math.ceil((float(data["site_long"])-68.7)/.05))
    serializer = SiteSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        # process_data(data)
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def site_search_view(request):
    searchText = request.query_params.get('searchText')
    print("searchText", searchText)
    queryset = Site.objects.filter(
        Q(location__icontains=searchText) | Q(priorityArea__icontains=searchText) | Q(district__icontains=searchText)
    )
    serializer = SiteSerializer(queryset, many=True)

    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_site_price(request):
    siteTag = request.query_params.get('siteTag')
    try:
        pricing = SitePricing.objects.get(site=siteTag)
    except ObjectDoesNotExist:
        return Response({"success":False, "data":"No Pricing Found"}, status=status.HTTP_400_BAD_REQUEST)    
    serializer = SitePricingSerializer(pricing)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])    
def post_site_pricing(request):
    data = request.data
    
    serializer = SitePricingSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
    print(serializer.errors, "errors")
    return Response({"success":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@parser_classes([MultiPartParser])
def images_from_ppt(request):
    print(request, "Presentation Object")
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
        return Response({"success":True, "data":{'images': sitesUploaded, 'notUploaded':slideNotUploaded}}, status=status.HTTP_201_CREATED)
    else:
        return Response({"success":True, "data":'some error happened'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser])
def get_site_images(request):
    siteTag = request.query_params.get('siteTag')
    print(siteTag)

    queryset = SiteImages.objects.filter(site=siteTag)[0]
    print(queryset)
    serializer = ImagePathsSerializer(queryset)
    image_data = None
    print(serializer.data["path"])
    with open(serializer.data["path"], 'rb') as f:
        image_data = f.read()
    response = HttpResponse(content_type='image/jpeg')
    response.write(image_data)
    return response
    

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
@parser_classes([MultiPartParser])
def upload_image_data(request):
    image_file = request.FILES.get('image')
    siteName = request.data.get('siteName')
    siteTag = request.data.get('siteTag')
    
    if image_file is None:
        return Response({'error': 'No file uploaded'}, status=400)

    images_folder = os.path.join(settings.STATIC_ROOT, 'ppt_images')
    
    if not os.path.exists(images_folder):
        os.makedirs(images_folder)

    now = datetime.now().strftime("%Y%m%dH%M%S")
    image_filename = os.path.join(images_folder, siteTag + now +".jpeg")
    image_bytes = image_file.read()
    with open(image_filename, 'wb') as f:
        f.write(image_bytes)
        print("File is written")
                
    serializer = ImagePathsSerializer(data={"siteName": siteName, "path": image_filename, "site":siteTag})
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True, "data":{"siteName": siteName, "path": image_filename, "site":siteTag}}, status=status.HTTP_201_CREATED)
    else:
        return Response({"success":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_all_bookings(request):
    booking = Booking.objects.all()
    serializer = BookingSerializer(booking, many=True)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_self_bookings(request):
    company = request.user.company.code
    booking = Booking.objects.filter(assigned_to=company)
    serializer = BookingSerializer(booking, many=True)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_booking(request):
    data = request.data
    serializer = BookingSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success":True, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def get_bookings_by_customer(request):
    searchText = request.query_params.get('customerID')
    queryset = Booking.objects.filter(assigned_to=searchText)
    serializer = BookingSerializer(queryset, many=True)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)

# class ImagesFetchSiteTagView(APIView):
#     def get(self, request):
#         searchText = request.query_params.get('siteTag')
#         queryset = SiteImages.objects.get(site_id=searchText)
#         serializer = ImagePathsSerializer(queryset)
#         print(serializer.data)
#         image_data = None    
#         with open(serializer.data["path"], 'rb') as f:
#             image_data = f.read()
#         response = HttpResponse(content_type='image/jpeg')
#         response.write(image_data)
#         return response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_nearby_assets(request):
    grid = request.query_params.get('grid')
    radius = request.query_params.get('radius', 5000)
    keyword = request.query_params.get('keyword')

    
    dataPoints = GoogleStats.objects.filter(Q(grid=grid) & Q(type=keyword))
    if len(dataPoints) > 0:
        serializer = GooglePlacesSerializer(dataPoints, many=True)
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)

    [latSpan, longSpan] = grid.split("_")
    lat_min =  8.4
    long_min = 68.7
    location = (lat_min+float(latSpan)*0.05-0.025, long_min+float(longSpan)*0.05-0.025)
    
    gmaps = googlemaps.Client("AIzaSyAmnjoE7eFekledKAqF8ctrMoNBk3w0Xm8")
    print(gmaps, "GMAPS REACHED HERE")
    places = gmaps.places_nearby(
        location=location,
        radius=radius,
        keyword=keyword
    )
    
    results = []

    for place in places['results']:
        result = {
            'grid':grid,
            'type':keyword,
            'name': place['name'],
            'address': place['vicinity'],
            'status':place['business_status'],
            'latitude': place['geometry']['location']['lat'],
            'longitude': place['geometry']['location']['lng'],
            'place_id': place['place_id']
        }
        serializer = GooglePlacesSerializer(data = result)
        if serializer.is_valid():        
            serializer.save()
            results.append(result)


    while True:
        time.sleep(2)
        if "next_page_token" not in places:
            break
        else:
            next_page_token = places["next_page_token"]  
        print(next_page_token, "next page token")
        places = gmaps.places_nearby(
            location=location,
            radius=radius,
            keyword=keyword,
            page_token=next_page_token
        )

        print(places, "next Page Data")
        for place in places['results']:
            result = {
                'grid':grid,
                'type':keyword,
                'name': place['name'],
                'address': place['vicinity'],
                'status':place['business_status'],
                'latitude': place['geometry']['location']['lat'],
                'longitude': place['geometry']['location']['lng'],
                'place_id': place['place_id']
            }
            serializer = GooglePlacesSerializer(data = result)
            if serializer.is_valid():        
                serializer.save()
                results.append(result)
            
        

    return Response({"success":True, "data":results}, status=status.HTTP_200_OK)
    


# class PlaceDetailAPI(APIView):
#     def get(self, request):
#         place_id = request.GET.get('place_id')
#         gmaps = googlemaps.Client("AIzaSyAmnjoE7eFekledKAqF8ctrMoNBk3w0Xm8")

#         place_details = gmaps.place(place_id=place_id)
#         return Response({"success":True, "data":place_details['result']}, status=status.HTTP_200_OK)
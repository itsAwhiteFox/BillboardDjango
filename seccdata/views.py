from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from .models import SeccData
from .serializers import SECCSerializer, RegionSerializer
    
@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_area(request):
    data = request.data
    serializer = SECCSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_area(request):
        searchText = request.query_params.get('searchText')
        queryset = SeccData.objects.filter(
            Q(State__icontains=searchText) | Q(District__icontains=searchText) | Q(SubDistrict__icontains=searchText)
        )
        serializer = SECCSerializer(queryset, many=True)
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def region_list(request):
        queryset = SeccData.objects.all()
        serializer = RegionSerializer(queryset, many=True)
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Q
from .models import Customer
from .serializers import CustomerSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def customer_detail(request):
    user = request.user
    #company = user.company.code    
    serializer = CustomerSerializer(user.company)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def customer_list(request):
    site = Customer.objects.all()
    serializer = CustomerSerializer(site, many=True)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def create_customer(request):
    user = request.user
    data = request.data
    data["createdBy"] = user
    print(data)
    serializer = CustomerSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminUser])
def search_customer(request):
        searchText = request.query_params.get('searchText')
        queryset = Customer.objects.filter(
            Q(customerName__icontains=searchText) | Q(address__icontains=searchText) | Q(poc__icontains=searchText)
        )
        serializer = CustomerSerializer(queryset, many=True)
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Customer
from .serializers import CustomerSerializer

class CustomersAPIView(APIView):

    def get(self, request, pk=None):
        if pk is not None:
            site = Customer.objects.get(pk=pk)
            serializer = CustomerSerializer(site)
            return Response(serializer.data)
        
        site = Customer.objects.all()
        serializer = CustomerSerializer(site, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = CustomerSerializer(data = data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


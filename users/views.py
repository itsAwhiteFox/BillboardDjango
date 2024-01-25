from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import CustomUser
from .serializers import CustomUserSerializer, CustomUserViewSerializer, PasswordResetSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])    
def reset_password(request):
    if request.method == 'POST':    
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']

            try:
                user = CustomUser.objects.filter(email=email)[0]
            except CustomUser.DoesNotExist:
                return Response({"success":False, 'data': 'User with this Email ID does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(password)
            user.save()
            return Response({"success":True,'data': 'Password reset successful.'}, status= status.HTTP_202_ACCEPTED)
    return Response({"success":False,'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def staff_list(request):
    # this needs to be changed along with 
    # the data in the user list
    if request.method == 'GET':
        users = CustomUser.objects.filter(is_staff=True)
        serializer = CustomUserViewSerializer(users, many=True)
        return Response({"success":True,'data': serializer.data}, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            CustomUser.objects.create_staff(**serializer.validated_data)
            return Response({"success":True,'data': serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"success":False,'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def users_list(request):

    user = request.user
    is_staff = user.is_staff
    
    if request.method == 'GET':
        if is_staff:
            users = CustomUser.objects.all()
        else:
            company = user.company.code
            users = CustomUser.objects.filter(company = company)
        serializer = CustomUserViewSerializer(users, many=True)
        return Response({"success":True,'data': serializer.data}, status= status.HTTP_200_OK)

    elif request.method == 'POST':
        data = request.data
        if not is_staff:
            company = user.company.code
            data["company"] = company  

        serializer = CustomUserSerializer(data = data)
        if serializer.is_valid():
            try:    
                CustomUser.objects.create_user(**serializer.validated_data)
                return Response({"success":True, "data": "User Created Successfully"}, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"success":False,'company': [str(e)]}, status=status.HTTP_400_BAD_REQUEST) 
        return Response({"success":False,'data': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_detail(request):
    user = request.user
    serializer = CustomUserViewSerializer(user)
    return Response({"success":True, "data": serializer.data},status=status.HTTP_200_OK)

    

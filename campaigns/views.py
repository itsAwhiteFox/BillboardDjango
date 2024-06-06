import uuid
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status

from .models import Campaigns
from sites.models import Site
from .serializers import CampaignsSerializer
from .printLayouts.printReport import printReportData
from django.http import HttpResponse


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_campaign_detail(request, pk):
    campaign = Campaigns.objects.get(pk=pk)
    serializer = CampaignsSerializer(campaign)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_campaign_list(request):
    campaigns = Campaigns.objects.prefetch_related("assignedSites").all()
    serializer = CampaignsSerializer(campaigns, many=True)
    return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def print_campaign_data(request, pk):
    campaign = Campaigns.objects.get(pk=pk)
    serializer = CampaignsSerializer(campaign)
    report = printReportData(serializer.data)
    print(report, "printReportData")
    # report.output('detailed_report.pdf')

    # print("serializer data", serializer.data)
    # print("raw data",campaign)
    response = HttpResponse(report, content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="detailed_report.pdf"'
    return response


    #return Response({"success":True, "data":serializer.data}, status=status.HTTP_200_OK)



@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def post_new_campaign(request):
    data = request.data
    data["code"] = str(uuid.uuid4())
    serializer = CampaignsSerializer(data = data)
    if serializer.is_valid():
        serializer.save()
        return Response({"success":True, "data":serializer.data}, status=status.HTTP_201_CREATED)
    return Response({"success":False, "data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def add_site_to_campaign(request, pk):
    print(pk)
    try:
        campaign = Campaigns.objects.get(pk=pk)
    except campaign.DoesNotExist:
        return Response({"success":False, "data": 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
    
    site_ids = request.data.get('site_ids', [])
    try:
        sites = Site.objects.filter(siteTag__in=site_ids)
    except Site.DoesNotExist:
        return Response({"success":False,'data': 'One or more sites not found'}, status=status.HTTP_404_NOT_FOUND)
    
    campaign.assignedSites.add(*sites)
    return Response({"success":True, 'data': 'Sites added to campaign successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated, IsAdminUser])
def remove_site_from_campaign(request, pk):
    print(pk)
    try:
        campaign = Campaigns.objects.get(pk=pk)
    except campaign.DoesNotExist:
        return Response({"success":False, "data": 'Campaign not found'}, status=status.HTTP_404_NOT_FOUND)
    
    site_id = request.data.get('site_id')
    try:
        site = Site.objects.get(siteTag=site_id)
    except Site.DoesNotExist:
        return Response({"success":False,'data': 'Site not found'}, status=status.HTTP_404_NOT_FOUND)
    
    campaign.assignedSites.remove(site)
    return Response({"success":True, 'data': 'Sites removed from campaign successfully'}, status=status.HTTP_200_OK)
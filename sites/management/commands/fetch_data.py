from django.core.management.base import BaseCommand
from django.db.models import Subquery, OuterRef
import requests
import random
import time
from sites.models import GoogleTrafficStats
from django.db.models import Min
import logging
from django.utils import timezone


logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Fetch and store data from an external source'
    logger.info("Starting data fetching process...")


    def handle(self, *args, **options):
        twenty_four_hours_ago = timezone.now() - timezone.timedelta(hours=24)
        unique_sites = GoogleTrafficStats.objects.filter(created__gte=twenty_four_hours_ago).values('site').annotate(oldest_entry=Min('created'))

        for site_row in unique_sites:
            site = GoogleTrafficStats.objects.filter(site=site_row["site"], created=site_row["oldest_entry"]).first()
            print(site)
            siteTag = site.site
            origin = f"{site.latitude_1},{site.longitude_1}"
            destination = f"{site.latitude_2},{site.longitude_2}"
            url = "https://maps.googleapis.com/maps/api/distancematrix/json"
            params = {
            "departure_time":"now",
            "origins": origin,
            "destinations": destination,
            "key": "AIzaSyAmnjoE7eFekledKAqF8ctrMoNBk3w0Xm8"
            }

            response = requests.get(url, params=params)
            data = response.json()

            # Save data to database
            GoogleTrafficStats.objects.create(
            site = siteTag,
            latitude_1=site.latitude_1,
            longitude_1=site.longitude_1,
            latitude_2=site.latitude_2,
            longitude_2=site.longitude_2,
            distance=data['rows'][0]['elements'][0]['distance']['value'],
            average_time=data['rows'][0]['elements'][0]['duration']['value'],
            traffic_time=data['rows'][0]['elements'][0]['duration_in_traffic']['value'],
            )

        logger.info("ending data fetching process...")

        self.stdout.write(self.style.SUCCESS('Data fetched and stored successfully'))

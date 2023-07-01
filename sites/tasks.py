import dramatiq
import googlemaps

from .models import SiteGoogleStats, Site

@dramatiq.actor
def process_data(data):
    list = ["atm", "bank", "beauty_salon", "cafe", "convenience_store", "department_store", "gym", "hospital", "park", "restaurant", "school", "shopping_mall", "supermarket"]
    location = str(data["site_lat"])+","+str(data["site_long"])
    radius = 1000
    siteInstance = Site.objects.get(siteTag = data["siteTag"])
    gmaps = googlemaps.Client("AIzaSyAmnjoE7eFekledKAqF8ctrMoNBk3w0Xm8")
    
    for item in list:
        places = gmaps.places_nearby(
            location=location,
            radius=radius,
            keyword=item
        )

        results = []
        for place in places['results']:
            
            SiteGoogleStats.objects.create(
                site = siteInstance,
                type =item,
                name = place['name'],
                address = place['vicinity'],
                status =place['business_status'],
                latitude = place['geometry']['location']['lat'],
                longitude = place['geometry']['location']['lng'],
                place_id = place['place_id']
                )
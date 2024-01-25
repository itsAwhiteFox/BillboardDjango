import googlemaps
import time
from .models import GoogleStats, Site

def process_data(data):
    list = ["atm", "bank", "beauty_salon", "cafe", "convenience_store", "department_store", "gym", "hospital", "park", "restaurant", "school", "shopping_mall", "supermarket"]
    location = str(data["site_lat"])+","+str(data["site_long"])
    radius = 1000
    siteInstance = Site.objects.get(siteTag = data["siteTag"])
    gmaps = googlemaps.Client("AIzaSyAmnjoE7eFekledKAqF8ctrMoNBk3w0Xm8")
    
    def getPlaces(location, radius, item):
        places = gmaps.places_nearby(
            location=location,
            radius=radius,
            keyword=item,
        )
        return places
    
    def getPlacesNext(location, radius, item, token):
        places = gmaps.places_nearby(
            location=location,
            radius=radius,
            keyword=item,
            page_token=str(token)
        )
        return places


    for item in list:
        results = []
        next_page_token = None
        while True:
            if not next_page_token:
                places = getPlaces(location, radius, item)
                results = results + places["results"]
                if "next_page_token" in places:
                    next_page_token = places["next_page_token"]
            else:
                print("next page", item)
                time.sleep(2)
                places = getPlacesNext(location, radius, item, next_page_token)
                results = results + places["results"]
                if "next_page_token" in places:
                    next_page_token = places["next_page_token"]
                else:
                    next_page_token=None
            if not next_page_token:
                break

        for place in results:
            
            GoogleStats.objects.create(
                site = siteInstance,
                type =item,
                name = place['name'],
                address = place['vicinity'],
                status =place['business_status'],
                latitude = place['geometry']['location']['lat'],
                longitude = place['geometry']['location']['lng'],
                place_id = place['place_id']
                )
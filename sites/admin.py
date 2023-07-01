from django.contrib import admin
from .models import Site, Booking, SiteImages
# Register your models here.

admin.site.register(Site)
admin.site.register(Booking)
admin.site.register(SiteImages)
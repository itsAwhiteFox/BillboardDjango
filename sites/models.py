from django.db import models
from customers.models import Customer
from users.models import CustomUser

class Site(models.Model):
    siteTag = models.CharField(max_length=200, unique=True)
    town = models.CharField(max_length=200)
    priorityArea = models.CharField(max_length=200, null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    media = models.CharField(max_length=50)
    media_type = models.CharField(max_length=50)
    size_width = models.IntegerField()
    size_height = models.IntegerField()
    site_lat = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    site_long = models.DecimalField(max_digits=9, decimal_places=6, default=0)
    created = models.DateTimeField(auto_now_add=True)
    

class SitePricing(models.Model):
    site = models.OneToOneField(Site, on_delete=models.RESTRICT, blank = True, null = True, to_field='siteTag')
    cost_monthly = models.IntegerField()
    printing_cost = models.IntegerField()
    mounting_cost = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

class Booking(models.Model):
    site = models.ForeignKey(Site, on_delete=models.RESTRICT, blank = True, null = True, to_field='siteTag')
    alloted_on = models.DateField()
    duration = models.IntegerField()
    assigned_to = models.ForeignKey(Customer, on_delete=models.RESTRICT, blank = True, null = True)
    applicablePrice = models.IntegerField()
    salesPrice = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    

class SiteImages(models.Model):
    site = models.OneToOneField(Site, on_delete=models.RESTRICT, blank = True, null = True, to_field='siteTag')
    siteName = models.CharField(max_length=200)
    path = models.CharField(max_length = 500)    
    created = models.DateTimeField(auto_now_add=True)

class SiteGoogleStats(models.Model):
    site = models.ForeignKey(Site, on_delete=models.RESTRICT, blank = True, null = True, to_field='siteTag')
    type = models.CharField(max_length=200)
    name = models.CharField(max_length = 200)
    address = models.CharField(max_length = 500)
    status = models.CharField(max_length = 200)
    latitude = models.DecimalField(max_digits=24, decimal_places=21,default=0)
    longitude = models.DecimalField(max_digits=24, decimal_places=21,default=0)
    place_id = models.CharField(max_length = 200)    
    created = models.DateTimeField(auto_now_add=True)

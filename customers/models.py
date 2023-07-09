from django.db import models
from users.models import CustomUser

class Customer(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    customerCode = models.CharField(max_length=21, default='', unique=True)
    customerName = models.CharField(max_length=101, default='')
    customerGST = models.CharField(max_length=51, default='')
    address = models.CharField(max_length=201)
    district = models.CharField(max_length=101, default='')
    state = models.CharField(max_length=101, default='')
    pincode = models.CharField(max_length=101, default='')
    poc = models.CharField(max_length=101, default='')
    email = models.EmailField(max_length=101, default='')
    contact = models.CharField(max_length=101, default='')
    
    class Meta:
        ordering = ['created']


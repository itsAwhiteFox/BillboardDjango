from django.db import models

class Customer(models.Model):
    code = models.CharField(primary_key=True, max_length=21, default='')
    created = models.DateTimeField(auto_now_add=True)
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

    def __str__(self):
        return f'{self.customerName}, {self.poc}, {self.email}'




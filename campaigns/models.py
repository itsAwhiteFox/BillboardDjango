from django.db import models
from customers.models import Customer
from sites.models import Site

class Campaigns(models.Model):
    code = models.CharField(primary_key=True, max_length=100, default='')
    campaignName = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    assigned_customer = models.ForeignKey(Customer, on_delete=models.RESTRICT, blank = True, null = True)
    startDate = models.DateField()
    endDate = models.DateField()
    assignedSites = models.ManyToManyField(Site)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f'{self.campaignName}, {self.startDate}, {self.endDate}'




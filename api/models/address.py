from django.db import models
from .profile import Employee

# from django_countries.fields import CountryField

ADDRESS_TYPE = ((1, 'Home'),
                (2, 'Permanent'))


class Address(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='addresses', null=True)
    address_type = models.IntegerField(choices=ADDRESS_TYPE, default=1)
    house = models.CharField(max_length=255, null=True, blank=True)
    road = models.CharField(max_length=255, null=True, blank=True)
    village = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    zip = models.CharField(max_length=50, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


class Education(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='educations', null=True)
    degree = models.CharField(max_length=250)
    graduate_date = models.DateField()
    subject = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

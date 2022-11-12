from django.db import models
from django.contrib.auth.models import User
from commerce.models import *



class Userprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profilepic = models.ImageField(null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.profilepic.url
        except:
            url = ''
        return url


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    address = models.TextField(max_length=500)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.IntegerField()


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product_batch = models.ForeignKey(ProductBatch, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    totalprice = models.IntegerField(null=True, blank=True, default=0)

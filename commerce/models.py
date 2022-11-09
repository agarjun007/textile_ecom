from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    categoryname = models.CharField(max_length=50)

class products(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    productname = models.CharField(max_length=20)
    productdesc = models.TextField(max_length=5000)
    price = models.IntegerField()
    Quantity = models.IntegerField()
    unit = models.CharField(max_length=20,null=True)
    productimage = models.ImageField(null=True, blank=True)

    @property
    def ImageURL(self):
        try:
            url = self.productimage.url
        except:
            url = ''
        return url
        


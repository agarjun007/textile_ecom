from django.db import models
from django.contrib.auth.models import User

#declaring variables as public
INACTIVE,ACTIVE = 0,1


class Category(models.Model):
    categoryname = models.CharField(max_length=50)
    status = models.IntegerField(db_column="status", default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")
    deleted_at = models.DateTimeField(db_column="deleted_at", blank=True, null=True)

class products(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products')
    productname = models.CharField(max_length=20)
    productdesc = models.TextField(max_length=5000)
    status = models.IntegerField(db_column="status", default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")
    deleted_at = models.DateTimeField(db_column="deleted_at", blank=True, null=True)

class Size(models.Model):
    name = models.CharField(max_length=20) #eg: M/XL/XXL/XXXL/34/36,38,40
    status = models.IntegerField(db_column="status", default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")
    deleted_at = models.DateTimeField(db_column="deleted_at", blank=True, null=True)

class Color(models.Model):
    name = models.CharField(max_length=20) # eg: black
    color_code = models.CharField(max_length=15) #eg: #00000F
    status = models.IntegerField(db_column="status", default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")
    deleted_at = models.DateTimeField(db_column="deleted_at", blank=True, null=True)
            

class ProductBatch(models.Model):
    product = models.ForeignKey(products,on_delete=models.CASCADE,related_name='batches')
    size = models.ForeignKey(Size,on_delete=models.DO_NOTHING,related_name='batches')
    color = models.ForeignKey(Color,on_delete=models.DO_NOTHING, null=True, blank=True,related_name='batches')
    embroidery = models.BooleanField(default=False)
    emb_price = models.IntegerField(default=0)
    price = models.IntegerField()
    quantity = models.IntegerField()
    unit = models.CharField(max_length=20,null=True) #eg: no.s 
    default = models.BooleanField(default=True)
    status = models.IntegerField(default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")
    deleted_at = models.DateTimeField(db_column="deleted_at", blank=True, null=True)

    @property
    def ImageURL(self):
        try:
            url = self.productimage.url
        except:
            url = ''
        return url
        
class ProductImages(models.Model):
    product_batch = models.ForeignKey(ProductBatch,on_delete=models.DO_NOTHING,related_name='images')
    productimage = models.ImageField(null=True, blank=True)
    status = models.IntegerField(db_column="status", default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True, db_column="created_at")
    updated_at = models.DateTimeField(auto_now=True, db_column="updated_at")
    deleted_at = models.DateTimeField(db_column="deleted_at", blank=True, null=True)

    @property
    def ImageURL(self):
        try:
            url = self.productimage.url
        except:
            url = ''
        return url
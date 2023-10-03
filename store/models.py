from django.db import models
from django.utils.text import slugify

from stats.models import Server

class Product(models.Model):
    class MethodChoices(models.TextChoices):
            KHALTI = "KHALTI", "KHALTI"
            STRIPE = "STRIPE", "STRIPE"
    title = models.CharField(max_length=64)
    price = models.PositiveIntegerField(help_text='Enter in paisa. ie Rs 10 is 1000')
    server = models.ForeignKey(Server,on_delete=models.SET_NULL,null=True,related_name='products')
    duration = models.PositiveSmallIntegerField()
    slug = models.SlugField(unique=True,blank=True)
    payment_method = models.CharField(max_length=64,choices=MethodChoices.choices,default=MethodChoices.KHALTI)

    def __str__(self):
        return self.title

    def save(self,*args, **kwargs):
        slug = f"{self.server.display_name}-{self.duration}D"
        self.slug = slugify(slug)
        super().save(*args, **kwargs)
    
    def in_stock(self):
        return self.server.product_in_stock()
    
    def f_price(self):
        return self.price // 100

class Purchase(models.Model):
    """
        DEPRECATED.
        Only kept to not delete old purchase records
    """
    buyer = models.CharField(max_length=54,null=True)
    receiver = models.CharField(max_length=54,null=True)
    idx = models.CharField(max_length=128)
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.idx

class StripePurchase(models.Model):
    buyer = models.CharField(max_length=54,null=True)
    receiver = models.CharField(max_length=54,null=True)
    idx = models.CharField(max_length=128)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.idx

class KhaltiPurchase(models.Model):
    buyer = models.CharField(max_length=54,null=True)
    receiver = models.CharField(max_length=54,null=True)
    idx = models.CharField(max_length=128)
    pidx = models.CharField(max_length=128)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return self.idx

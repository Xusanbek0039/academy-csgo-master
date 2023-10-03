from django.contrib import admin

from .models import Product, Purchase
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title','slug','duration','price',)
    search_fields = ('title',)

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('receiver','buyer','date_created',)
    search_fields = ('receiver',)


admin.site.register(Product,ProductAdmin)
admin.site.register(Purchase,PurchaseAdmin)
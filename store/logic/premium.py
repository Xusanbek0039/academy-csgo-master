import datetime
from stats.models import Vip
from store.models import Product, KhaltiPurchase, StripePurchase

def add_vip(product_slug,idx,steamid,steamid64,name,avatar,**kwargs):
    product = Product.objects.get(slug=product_slug)
    expires_date = datetime.timedelta(days=product.duration) + datetime.date.today()
    
    if product.payment_method == product.MethodChoices.KHALTI:
        KhaltiPurchase.objects.create(idx=idx,product=product,receiver=steamid,**kwargs)
    elif product.payment_method == product.MethodChoices.STRIPE:
        StripePurchase.objects.create(idx=idx,product=product,receiver=steamid,**kwargs)

    obj,created = Vip.objects.get_or_create(steamid=steamid,server=product.server,
                                            defaults={'expires':expires_date,
                                            'name':name,'steamid64':steamid64,'avatar':avatar})

    # Renew if not created new VIP entry
    if not created:
        obj.expires = obj.expires + datetime.timedelta(days=product.duration)
        obj.save()

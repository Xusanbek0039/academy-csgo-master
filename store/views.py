from django.conf import settings
from django.shortcuts import get_object_or_404, redirect
from django.http.response import HttpResponse
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.http import Http404
from django.urls import reverse
import stripe
from django.utils.decorators import method_decorator
from stats.models import Vip
from store.models import StripePurchase
from stats.models import Server
from stats.resolver import get_playerinfo,get_steamid
from django.views.decorators.csrf import csrf_exempt
from .models import Product
from .logic import premium,khalti

stripe.api_key = settings.STRIPE_SK

class PremiumStore(ListView):
    template_name = 'store/premium_store.html'
    queryset = Server.objects.filter(selling_premium=True)
    context_object_name = 'servers'
    
    def post(self,request,*args, **kwargs):
        try:
            steamid = get_playerinfo(request.POST.get('steamid'))
        except:
            messages.add_message(request,messages.ERROR,'Error Fetching SteamID',extra_tags='Failure')
            return redirect('store:index')
        if not steamid:
            messages.add_message(request,messages.ERROR,'Error Fetching SteamID',extra_tags='Failure')
            return redirect('store:index')
        product = request.POST.get('product','error')
        return redirect('store:checkout',slug=product,steamid=steamid.get('steamid','error'))    

class CheckoutView(DetailView):
    template_name = 'store/checkout.html'
    model = Product
    context_object_name = 'product'
    
    def dispatch(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model,slug=kwargs.get('slug'))
        steamid64 = kwargs.get('steamid')
        if not obj.in_stock():
            vip = Vip.objects.filter(steamid64=steamid64,server=obj.server)
            if not vip.exists():
                messages.add_message(self.request,messages.INFO,'Product Out Of Stock','Failure')
                return redirect('store:index')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        steamid = self.kwargs.get('steamid')
        context['profile'] = get_playerinfo(steamid)
        return context
    

class KhaltiVerifyView(View):
    """
        Deprecated
    """
    url = 'https://khalti.com/api/v2/payment/verify/'

    def post(self,request,*args, **kwargs):
        data = request.POST
        product_pk = data.get('product_identity')
        product = Product.objects.get(slug=product_pk)
        
        if not product.in_stock():
            return HttpResponse(status=400)

        response = khalti.verify_khalti(token=data.get('token'),amount=data.get('amount'))


        if not response.get('success'):                                     # If the provided token is invalid return HTTP 400
            return HttpResponse(status=400)

        profile = get_playerinfo(data.get('merchant_extra'))
        if request.user.is_authenticated:
            premium.add_vip(response['data']['product_identity'],response['data']['idx'],
                            get_steamid(profile['steamid']),profile['steamid'],profile['personaname'],profile['avatarfull'],**{'buyer':request.user})
        else:
            premium.add_vip(response['data']['product_identity'],response['data']['idx'],
                            get_steamid(profile['steamid']),profile['steamid'],profile['personaname'],profile['avatarfull'])
            
        return HttpResponse(status=200)
class StripeCheckoutView(View):
    def post(self, *args, **kwargs):
        product = self.get_object(self.kwargs.get("slug"))
        steamid = self.kwargs.get("steamid")
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency':'USD',
                        'product_data':{
                            'name':product.title,
                        },
                        'unit_amount':product.price
                    },
                    'quantity': 1,
                },
            ],
            client_reference_id=steamid,
            metadata={'slug':product.slug},
            mode='payment',
            success_url=settings.SITE_URL + reverse("store:checkout_stripe_done"),
            cancel_url=settings.SITE_URL + reverse("store:checkout",args=[product.slug,steamid]),
        )
        return redirect(checkout_session.url, code=303)

    def get_object(self, slug):
        product = Product.objects.filter(slug=slug).first()
        if not product:
            print("Product not found {}".format(slug))
            raise Http404()
        return product

@method_decorator(csrf_exempt,"dispatch")
class StripeCheckoutDoneView(View):

    def get(self,*args,**kwargs):
        messages.success(self.request,"Premium purchase successful","success")
        return redirect("stats:premium")
    
    def post(self,*args,**kwargs):
        payload = self.request.body
        sig_header = self.request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WH_SECRET
            )
        except ValueError as e:
            # Invalid payload
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            # Invalid signature
            return HttpResponse(status=400)

        id = event['data']['object']['payment_intent']
        # Check if a duplicate request
        if StripePurchase.objects.filter(idx=id).exists():
            return HttpResponse(status=400)

        if event['type'] == 'checkout.session.completed':
            # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
            session = stripe.checkout.Session.retrieve(
            event['data']['object']['id'],
            expand=['line_items'],
            )
            profile = get_playerinfo(session.client_reference_id)
            product_slug = session.metadata['slug']
            if self.request.user.is_authenticated:
                premium.add_vip(product_slug,id,
                                get_steamid(profile['steamid']),profile['steamid'],profile['personaname'],profile['avatarfull'],**{'buyer':self.request.user})
            else:
                premium.add_vip(product_slug,id,
                                get_steamid(profile['steamid']),profile['steamid'],profile['personaname'],profile['avatarfull'])

        return HttpResponse(status=200)

class KhaltiCheckoutView(View):
    def get(self,*args,**kwargs):
        product_slug = self.kwargs.get("slug")
        steamid = self.kwargs.get("steamid")
        product = Product.objects.filter(slug=product_slug).first()
        pidx, payment_url = khalti.KhaltiV2.initiate_payment(product.price,steamid,product.slug)
        return redirect(payment_url)

class KhaltiCheckoutDoneView(View):

    def get(self, *args, **kwargs):
        params = self.request.GET
        try:
            pidx = params['pidx']
            product_slug = params['purchase_order_name']
            steamid = params['purchase_order_id']
            tidx = params['transaction_id']
        except Exception as e:
            raise e

        resp = khalti.KhaltiV2.verify_payment(pidx)
        print(resp)
        if resp.get('success'):
            profile = get_playerinfo(steamid)
            if self.request.user.is_authenticated:
                premium.add_vip(product_slug,tidx,
                                get_steamid(profile['steamid']),profile['steamid'],profile['personaname'],
                                profile['avatarfull'],**{'buyer':self.request.user,'pidx':pidx})
            else:
                premium.add_vip(product_slug,tidx,
                                get_steamid(profile['steamid']),profile['steamid'],profile['personaname'],profile['avatarfull'],**{'pidx':pidx})
            messages.success(self.request,"Premium purchase successful","success")
            return redirect("stats:premium")
        else:
            messages.error(self.request,"Premium purchase failed. Please contact an admin for further info","failure")
            return redirect("store:index")

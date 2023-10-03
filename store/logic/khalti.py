from django.conf import settings
import requests
from django.urls import reverse_lazy

def verify_khalti(token,amount):
    payload = {
        'token':token,
        'amount':amount
        }
    key = settings.KHALTI_API_SECRET_KEY
    url = 'https://khalti.com/api/v2/payment/verify/'
    headers = {"Authorization": f"Key {key}"}
    r = requests.post(url,payload,headers=headers,timeout=3)
    r = r.json()
    response = {}
    if r.get('validation_error',None):
        response['success'] = False
        response['data'] = r
    else:
        response['success'] = True
        response['data'] = r
    return response

class KhaltiV2:
    """
        Khalti API wrapper:
        https://docs.khalti.com/khalti-epayment
    """

    base_url = "https://khalti.com/api/v2/"
    key = settings.KHALTI_API_SECRET_KEY
    
    @classmethod
    def construct_url(cls, path):
        return cls.base_url + path

    @classmethod
    def initiate_payment(cls, amt, purchase_ord_id, purchase_ord_name):
        path = "epayment/initiate/"
        url = cls.construct_url(path)
        return_url = settings.SITE_URL + reverse_lazy("store:checkout_khalti_done")
        payload = {
            "return_url": return_url,
            "website_url": settings.SITE_URL,
            "amount": amt,
            "purchase_order_id": purchase_ord_id,
            "purchase_order_name": purchase_ord_name,
        }
        headers = {"Authorization": f"Key {cls.key}"}
        resp = requests.post(url,payload,headers=headers)
        resp = resp.json()
        return resp['pidx'], resp['payment_url']

    @classmethod
    def verify_payment(cls, pidx):
        path = "epayment/lookup/"
        url = cls.construct_url(path)
        payload = {
            "pidx": pidx
        }
        headers = {"Authorization": f"Key {cls.key}"}
        resp = requests.post(url,payload,headers=headers)
        resp = resp.json()
        response = {}
        if resp.get('status') == 'Completed':
            response['success'] = True
            response['data'] = resp
        else:
            response['success'] = False
            response['data'] = resp
        return response

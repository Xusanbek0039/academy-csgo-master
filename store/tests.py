from django.test import TestCase
from django.test import Client
from django.urls import reverse
from stats.models import Server
from store.models import Product

# class TestStoreView(TestCase):

#     def setUp(self) -> None:
#         self.c = Client()
#         self.url = reverse('store:index')
#         server = Server.objects.create(
#                                         display_name='TEST',
#                                         db_identifier='TEST',
#                                         server_hostname="127.0.0.1:80",
#                                         selling_premium=True,
#                                         )
#         product = Product.objects.create(
#                                         title='TEST',
#                                         price=1000,
#                                         server=server,
#                                         duration=30,
#                                         )
#         self.data = {'steamid':'76561198323043075','product':product.slug}
#         self.redirect_url = reverse('store:checkout',kwargs={'steamid':'76561198323043075','slug':product.slug})

#     def test_get(self):
#         response = self.c.get(self.url)
#         self.assertEqual(response.status_code,200)

# class TestCheckoutView(TestCase):
#     def setUp(self) -> None:
#         self.c = Client()
#         server = Server.objects.create(
#                                         display_name='TEST',
#                                         identifier='TEST',
#                                         db_identifier='TEST',
#                                         ip='127.0.0.1',
#                                         port=80,
#                                         hide=False,
#                                         selling_premium=True,
#                                         )
#         product = Product.objects.create(
#                                         title='TEST',
#                                         price=1000,
#                                         server=server,
#                                         duration=30,
#                                         )
#         self.url = reverse('store:checkout',kwargs={'steamid':'76561198323043075','slug':product.slug})
#         self.data = {'steamid':'76561198323043075','product':product.slug}

#     def test_get(self):
#         response = self.c.get(self.url)
#         self.assertEqual(response.status_code,200)
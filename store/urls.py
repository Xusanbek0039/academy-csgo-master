from django.urls import path

from . import views

app_name = 'store'

urlpatterns = [
    path('', views.PremiumStore.as_view(),name='index'),
    path('checkout/<slug:slug>/<str:steamid>/', views.CheckoutView.as_view(),name='checkout'),
    path('checkout-stripe/<slug:slug>/<str:steamid>/', views.StripeCheckoutView.as_view(),name='checkout_stripe'),
    path('checkout-stripe-done/', views.StripeCheckoutDoneView.as_view(),name='checkout_stripe_done'),
    path('checkout-khalti/<slug:slug>/<str:steamid>/',views.KhaltiCheckoutView.as_view(),name='checkout_khalti'),
    path('checkout-khalti-done/',views.KhaltiCheckoutDoneView.as_view(),name='checkout_khalti_done'),
    path('verify/', views.KhaltiVerifyView.as_view(),name='khalti_verification_url')
]

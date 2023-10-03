from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar
urlpatterns = [
    path('',include('stats.urls')),
    path('store/',include('store.urls')),
    path('academy-admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('__debug__/', include(debug_toolbar.urls)),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

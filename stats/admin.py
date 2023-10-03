from django.contrib import admin
from . import models

class ServerAdmin(admin.ModelAdmin):
    list_display = ('display_name','selling_premium','hide',)
    list_filter = ('selling_premium','hide',)
    exclude = ('slug',)

class VipAdmin(admin.ModelAdmin):
    list_display = ('name','steamid','steamid64','expires','server')
    search_fields = ('name','steamid64',)
    list_filter = ('expires','server',)


admin.site.register(models.Server,ServerAdmin)
admin.site.register(models.Vip,VipAdmin)
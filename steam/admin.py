from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('nickname', 'steamid64','is_staff',)
    search_fields = ('nickname',)

admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
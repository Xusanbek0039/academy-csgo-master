from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

class User(AbstractUser):
    def get_steamid(self):
        try:
            return self.social_auth.first()
        except:
            return 0

class Profile(models.Model):
    steamid64 = models.CharField(primary_key=True, max_length=17)
    avatar = models.URLField(null=True,blank=True)
    nickname = models.CharField(max_length=64,blank=True,null=True,db_collation='utf8mb4_general_ci')
    last_updated = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return str(self.steamid64)
    
    def get_absolute_url(self):
        return reverse("stats:profile", kwargs={"steamid64": self.steamid64})
    
    def get_steamid(self):
        y = int(self.steamid64) - 76561197960265728
        x = y % 2 
        return "STEAM_1:{}:{}".format(x, (y - x) // 2)

    def is_premium(self):
        return Vip.objects.filter(steamid64=self.steamid64).exists()

from stats.models import Vip
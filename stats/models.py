import datetime
from django.db import models
import urllib.parse
from django.utils.text import slugify

from steam.models import Profile
from django.db import connections
import dj_database_url
from stats.helpers import encrypt, decrypt

class Server(models.Model):
    display_name = models.CharField(max_length=128,unique=True,blank=False)
    icon = models.CharField(max_length=32,default="fas fa-skull-crossbones")
    db_identifier = models.CharField(max_length=128,unique=True,null=True,blank=False)
    server_hostname = models.CharField(max_length=512,help_text="can either be hostname or ip:port")
    hide = models.BooleanField(default=False)
    selling_premium = models.BooleanField(default=True)

    # Statistic database config
    stats_db_url = models.CharField(max_length=1024, blank=True,help_text=" 'mysql://USER:PASSWORD@HOST:PORT/NAME' , this will be encypted")

    def __str__(self):
        return f'{self.display_name}'
    
    @property
    def ip(self):
        try:
            return self.server_hostname.split(":")[0]
        except:
            return self.server_hostname

    @property
    def port(self):
        try:
            return int(self.server_hostname.split(":")[-1])
        except:
            return 80

    def save(self,*args, **kwargs):
        url = self.parse_raw_db_url(self.stats_db_url)
        self.stats_db_url = url
        super().save(*args, **kwargs)
        self.add_db_to_conn_pool()

    def product_in_stock(self):
        q = Vip.objects.filter(server=self).count()
        return True if q < 15 else False

    def get_db_config(self):
        stats_db_url = decrypt(self.stats_db_url)
        db = dj_database_url.parse(stats_db_url,conn_max_age=600)
        db['OPTIONS'] = {'charset': 'utf8mb4'} 
        return db

    def add_db_to_conn_pool(self):
        if self.stats_db_url:
            connections.databases[self.display_name]= self.get_db_config()

    @classmethod
    def normalize_db_url(self, url):
        return urllib.parse.quote(url,safe='/,:,@')

    @classmethod
    def parse_raw_db_url(cls, url):
        if url:
            try:
                normalized_url = cls.normalize_db_url(url)
                dj_database_url.parse(normalized_url)
                url = encrypt(normalized_url)
            except Exception as e:
                print("Unchanged")
            return url

def get_expiry():
    return datetime.date.today() + datetime.timedelta(days=30)

class Vip(models.Model):
    name = models.CharField(max_length=128)
    steamid = models.CharField(max_length=256)
    steamid64 = models.CharField(max_length=128)
    avatar = models.URLField(null=True,blank=True)
    dateofpurchase = models.DateField(default=datetime.date.today)
    expires = models.DateField(default=get_expiry)
    server = models.ForeignKey(Server,on_delete=models.SET_NULL,null=True)

    class Meta:
        ordering = ('expires',)

    def __str__(self):
        return self.name

    def save(self,*args, **kwargs):
        super().save(*args,**kwargs)
        profile = Profile.objects.filter(steamid64=self.steamid64)
        flag = 'ao'
        if profile.exists():
            if profile.first().is_staff:
                flag = 'abcdego'

        obj , created = SmAdmins.objects.using(self.server.display_name).get_or_create(authtype='steam',identity=self.steamid,
                                                defaults={'flags':flag,'name':self.name,'immunity':0})
        if not created:
            obj.flags = flag
            obj.save()
            
    def delete(self,*args, **kwargs):
        q = SmAdmins.objects.using(self.server.display_name).get(authtype='steam',identity=self.steamid)
        profile = Profile.objects.filter(steamid64=self.steamid64)
        if profile.exists():
            if profile.first().is_staff:
                flag = 'bcdego'
                q.flags = flag
                q.save()
            else:
                q.delete()
        else:
            q.delete()

        super().delete(*args, **kwargs)


    def to_expire(self):
        delta= self.expires - datetime.date.today()
        return delta.days



class LvlBase(models.Model):
    steam = models.CharField(primary_key=True, max_length=22, db_collation='utf8_unicode_ci')
    name = models.CharField(max_length=32)
    value = models.IntegerField()
    rank = models.IntegerField()
    kills = models.IntegerField()
    deaths = models.IntegerField()
    shoots = models.IntegerField()
    hits = models.IntegerField()
    headshots = models.IntegerField()
    assists = models.IntegerField()
    round_win = models.IntegerField()
    round_lose = models.IntegerField()
    playtime = models.IntegerField()
    lastconnect = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'lvl_base'

    def __str__(self):
        return self.name

    def get_playtime(self):
        pt = self.playtime // 3600
        return pt
    
    def get_steamid64(self):
        x , y , z = self.steam.split(':')
        return int(z) * int(2) + int(y) + 76561197960265728
    
    def get_kd(self):
        kills = self.kills
        deaths = self.deaths
        try:
            return round(int(kills) / int(deaths),2)
        except (ValueError, ZeroDivisionError):
            return 0
    
    def get_accuracy(self):
        shoot = self.shoots
        hit = self.hits
        try:
            return int(round((int(hit) / int(shoot)),2)*100)
        except (ValueError, ZeroDivisionError):
            return 0

class SmAdmins(models.Model):
    authtype = models.CharField(max_length=5)
    identity = models.CharField(max_length=65)
    password = models.CharField(max_length=65, blank=True, null=True)
    flags = models.CharField(max_length=30)
    name = models.CharField(max_length=65)
    immunity = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'sm_admins'
        constraints = [models.UniqueConstraint(fields=['authtype','identity'],name='unqiue_admin')]


class SmAdminsGroups(models.Model):
    admin_id = models.PositiveIntegerField(primary_key=True)
    group_id = models.PositiveIntegerField()
    inherit_order = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'sm_admins_groups'
        unique_together = (('admin_id', 'group_id'),)


class SmConfig(models.Model):
    cfg_key = models.CharField(primary_key=True, max_length=32)
    cfg_value = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'sm_config'


class SmGroupImmunity(models.Model):
    group_id = models.PositiveIntegerField(primary_key=True)
    other_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'sm_group_immunity'
        unique_together = (('group_id', 'other_id'),)


class SmGroupOverrides(models.Model):
    group_id = models.PositiveIntegerField(primary_key=True)
    type = models.CharField(max_length=7)
    name = models.CharField(max_length=32)
    access = models.CharField(max_length=5)

    class Meta:
        managed = False
        db_table = 'sm_group_overrides'
        unique_together = (('group_id', 'type', 'name'),)


class SmGroups(models.Model):
    flags = models.CharField(max_length=30)
    name = models.CharField(max_length=120)
    immunity_level = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'sm_groups'


class SmOverrides(models.Model):
    type = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=32)
    flags = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'sm_overrides'
        unique_together = (('type', 'name'),)
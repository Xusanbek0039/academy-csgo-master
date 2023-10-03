from django.core.management.base import BaseCommand
import datetime
from stats.models import Vip

def notify(days):
    return datetime.date.today() + datetime.timedelta(days=days)

class Command(BaseCommand):
    help = 'check and delete expired premium subs'

    def handle(self, *args, **kwargs):
        queryset = Vip.objects.filter(expires__lte = notify(-1))
        length = queryset.count()
        for obj in queryset:
            obj.delete()
        return f"{length} VIPs deleted"
from django.apps import AppConfig


class StatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stats'

    def ready(self):
        try:
            from .models import Server
            servers = Server.objects.all()
            for server in servers:
                server.add_db_to_conn_pool()
        except:
            pass
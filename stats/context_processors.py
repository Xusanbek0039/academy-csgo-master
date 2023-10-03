from .models import Server

def get_server(request):
    return {"servers_list":Server.objects.values("display_name","stats_db_url","icon")}
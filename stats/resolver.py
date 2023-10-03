from requests import get as request_get
from django.conf import settings
from django.core.exceptions import ValidationError

STEAM_API_KEY = settings.STEAM_WEB_API_KEY


def identify_steamid_type(profile_url:str) -> dict:
    if len(str(profile_url)) == 17:
        return {'type':'profiles','data':profile_url}

    profile_url = profile_url.strip('/')
    data = profile_url.split('/')

    if len(data) <=2:
        raise ValidationError(f'Invalid profile url:{profile_url}')

    if data[-3] != 'steamcommunity.com':
        raise ValidationError(f'Invalid profile url:{profile_url}')
    if data[-2] == 'id':
        return {'type':'id','data':data[-1]}
    elif data[-2] == 'profiles':
        return {'type':'profiles','data':data[-1]}
    else:
        raise ValidationError(f'Invalid profile url:{profile_url}')

def resolve_vanity_name(vanity_name:str) -> str:
    vanity_url = f'http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={vanity_name}'
    r = request_get(vanity_url,timeout=1)
    response = r.json()
    response_json = response['response']
    return response_json['steamid']

def get_playerinfo(profile_url):
    player_info_url = 'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={}&steamids={}'
    data = identify_steamid_type(profile_url)

    if data.get('type') == 'id':
        steamid64 = resolve_vanity_name(data.get('data'))
    elif data.get('type') == 'profiles':
        steamid64 = data.get('data')

    url = player_info_url.format(STEAM_API_KEY,steamid64)
    response = request_get(url,timeout=1)
    response = response.json()
    return response['response']['players'][0]

def get_steamid(sid):
    if len(str(sid)) != 17:
        return None
    try:
        y = int(sid) - 76561197960265728
    except:
        return None
    x = y % 2 
    return "STEAM_1:{}:{}".format(x, (y - x) // 2)
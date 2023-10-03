from django.core.exceptions import ValidationError
from django.test import TestCase
from . import resolver

class ResolverTestCase(TestCase):
    """
        Class to test functions in stats/resolvers.py
    """
    
    profile_url_profiles = 'https://steamcommunity.com/profiles/76561198323043075/'
    profile_url_profiles_type = 'profiles'
    profile_url_vanity = 'https://steamcommunity.com/id/theonionknight4400/'
    profile_url_vanity_type = 'id'
    profile_url_invalid = 'https://steamcommunity.com/poa/76561198323043075/'

    profile_vanity = 'theonionknight4400'
    profile_steamid64 = '76561198323043075'

    def test_identify_steamid_type(self):
        data_profiles = resolver.identify_steamid_type(self.profile_url_profiles)
        data_vanity = resolver.identify_steamid_type(self.profile_url_vanity)
        self.assertEqual(data_profiles.get('type'),self.profile_url_profiles_type)
        self.assertEqual(data_vanity.get('type'),self.profile_url_vanity_type)
    
    def test_resolve_vanity_name(self):
        data = resolver.resolve_vanity_name(self.profile_vanity)
        self.assertEqual(data,self.profile_steamid64)
    
    def test_get_playerinfo(self):
        data = resolver.get_playerinfo(self.profile_url_profiles)
        self.assertEqual(data.get('steamid'),self.profile_steamid64)
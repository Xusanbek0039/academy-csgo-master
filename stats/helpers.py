from cryptography.fernet import Fernet
from django.conf import settings

def encrypt(payload:str):
    return Fernet(settings.FERNET_KEY).encrypt(payload.encode()).decode('utf-8')

def decrypt(payload:str):
    return Fernet(settings.FERNET_KEY).decrypt(payload.encode()).decode('utf-8')

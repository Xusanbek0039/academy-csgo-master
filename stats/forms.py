from django import forms
from django.forms.widgets import Textarea
from .models import Server

class ReportPlayerForm(forms.Form):
    suspect_steam_id = forms.CharField(max_length=256,label="Suspect's Steam Profile URL",required=False)
    suspect_nickname = forms.CharField(max_length=64,label="Suspect's Steam Nickname",help_text="Suspect's most common nickname")
    self_name = forms.CharField(max_length=52,label='Your Name',required=False)
    self_email = forms.EmailField(label='Your Email',help_text='Please use a valid email, We use this to confirm an incident')
    server = forms.ModelChoiceField(queryset=Server.objects.filter(hide=False),help_text='Where the incident occurred')
    comment = forms.CharField(widget=forms.Textarea,label='Incident Statement',help_text="Throughly describe the suspect's wrongdoings")

class AppealBanForm(forms.Form):
    reason_choices = (('Griefing','Griefing'),('Toxicity','Toxicity'),('Unauthorized ads','Unauthorized ads'),('Use of hack or cheats','Use of hacks or cheats'))
    steam_id = forms.CharField(max_length=256,label="Your Steam Profile URL")
    name = forms.CharField(max_length=52,label='Your Name',required=False)
    email = forms.EmailField(label='Your Email',help_text='Please use a valid email')
    reason = forms.ChoiceField(choices=reason_choices,required=True)
    server = forms.ModelChoiceField(queryset=Server.objects.filter(hide=False),help_text='Where the incident occurred')
    comment = forms.CharField(widget=forms.Textarea,label='Apology Statement')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=64)
    email = forms.EmailField(help_text='Please use a valid email')
    phone = forms.CharField(max_length=15,help_text='Please enter your country code too',required=False)
    subject = forms.CharField(max_length=128)
    message = forms.CharField(widget=Textarea)
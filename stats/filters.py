import django_filters
from .models import LvlBase, Vip
from django.forms.widgets import TextInput

class VipFilter(django_filters.FilterSet):
    name = django_filters.CharFilter('name','icontains')

    class Meta:
        model = Vip
        fields = ('name',)

class LvlBaseFilter(django_filters.FilterSet):
    name = django_filters.CharFilter('name','icontains',label='',widget=TextInput(attrs={'placeholder':'Search By Name','class':'p-1 ms-1'}))

    class Meta:
        model = LvlBase
        fields = ('name',)
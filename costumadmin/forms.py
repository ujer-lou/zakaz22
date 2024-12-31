from django import forms

from costumadmin.models import Unit


class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['unit_num', 'unit_name', 'book']
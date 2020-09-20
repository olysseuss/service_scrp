from django import forms
from scrap.models import City, Language


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  to_field_name='slug',
                                  required=False,  # allows you to make a choice in the form optional
                                  widget=forms.Select(attrs={'class': 'form-control'}), # assign a class to the form(from Bootstrap)
                                  label='Город')
    language = forms.ModelChoiceField(queryset=Language.objects.all(),
                                      to_field_name='slug',
                                      required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}),
                                      label='Специальность')

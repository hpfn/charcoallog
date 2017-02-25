from django import forms
from datetime import date
from charcoallog.core.models import Extract

class EditExtractForm(forms.Form):
    """
    Form for individual user account
    """
    date_today = date.today()

    user_name = forms.CharField(max_length=30)
    date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': date_today.isoformat(),
    }),
    required=True)
    money = forms.FloatField(required=True)
    description = forms.CharField(max_length=70,
                                  widget=forms.TextInput(attrs={
                                      'placeholder': 'specific_place',
                                  }),
                                  required=True)
    category = forms.CharField(max_length=70,
                               widget=forms.TextInput(attrs={
                                   'placeholder': 'type of',
                               }),
                               required=True)
    payment = forms.CharField(max_length=70,
                              widget=forms.TextInput(attrs={
                                  'placeholder': 'account used',
                              }),
                              required=True)

    class Meta:
        model = Extract
        fields = ['user_name', 'date', 'money', 'description', 
                'category', 'payment']

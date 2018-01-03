from django import forms
from .models import Extract
from datetime import datetime

# more recent
# https://codedump.io/share/3seZkm5xb6mu/1/using-django-timedate-widgets-in-custom-form
# very old
# http://stackoverflow.com/questions/5449604/django-calendar-widget-in-a-custom-form
# needs to edit the template
# from django.contrib.admin.widgets import AdminDateWidget

# class CalendarWidget(forms.TextInput):
#    class Media:
#        css = {
#            'all': '/static/css/calendar-blue.css'
#        }
#        js = ('/static/jscalendar/calendar.min.js',
#              '/static/jscalendar/calendar-setup.min.js')


class EditExtractForm(forms.ModelForm):
    """
    Form for individual user account
    """
    CHOICES = (('update', '1',), ('remove', '2',))
    update_rm = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=False)
    pk = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Extract
        fields = ['user_name', 'date', 'money', 'description',
                  'category', 'payment']
        widgets = {
            'user_name': forms.HiddenInput(),
            'description': forms.TextInput(attrs={
                'placeholder': 'description'}),
            'category': forms.TextInput(attrs={
                'placeholder': 'category'}),
            'payment': forms.TextInput(attrs={
                'placeholder': 'account used'})
        }


class SelectExtractForm(forms.Form):
    """ Specific Columm """
    # user_name = forms.CharField(max_length=30, widget=forms.HiddenInput(),
    #                            required=True)
    d = datetime.now()
    year = int(d.strftime("%Y"))
    years = [x for x in range(year-5, year+10)]
    column = forms.CharField(max_length=70, required=True)
    from_date = forms.DateField(widget=forms.SelectDateWidget(years=years), required=True)
    to_date = forms.DateField(widget=forms.SelectDateWidget, required=True)

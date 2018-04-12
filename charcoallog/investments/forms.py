from django import forms

from charcoallog.investments.models import Investment


class InvestmentForm(forms.ModelForm):
    """ Pode passar o argumento 'label'"""
    # date = forms.DateField()
    # money = forms.DecimalField()
    # kind = forms.CharField()
    # which_target = forms.CharField()
    # tx_op = forms.DecimalField()
    # brokerage = forms.CharField()

    class Meta:
        model = Investment
        fields = ['user_name', 'date', 'money', 'kind',
                  'which_target', 'tx_op', 'brokerage']

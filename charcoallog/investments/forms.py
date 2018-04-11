from django import forms


class InvestmentForm(forms.Form):
    """ Pode passar o argumento 'label'"""
    date = forms.DateField()
    money = forms.DecimalField()
    kind = forms.CharField()
    which_target = forms.CharField()
    tx_op = forms.DecimalField()
    brokerage = forms.CharField()

    # class Meta:
    #     model = Investment
    #     fields = ['date', 'money', 'kind',
    #               'which_target, 'tx_op', 'brokerage']

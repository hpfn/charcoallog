from django import forms

from charcoallog.investments.models import BasicData, Investment


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
        fields = ['tx_op', 'brokerage']

    def save(self, basic_data, commit=True):
        form = super(InvestmentForm, self).save(commit=False)
        # form.user_name = self.cleaned_data['user_name']
        form.basic_data = basic_data

        if commit:
            form.save()

        return form


class BasicDataForm(forms.ModelForm):
    class Meta:
        model = BasicData
        fields = ['date', 'money', 'kind', 'which_target']

    def save(self, request_user, commit=True):
        form = super(BasicDataForm, self).save(commit=False)
        form.user_name = request_user

        if commit:
            form.save()

        return form

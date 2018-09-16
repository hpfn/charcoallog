from charcoallog.bank.models import Extract, Schedule

from .forms import EditExtractForm


class MethodPost:
    def __init__(self, request, query_user):
        """
        :param request: request from views
        :param query_user: Extract models instance
        """
        # self.request_method = request_method
        self.request_post = request.POST
        self.request_user = request.user
        self.query_user = query_user
        self.editextractform = EditExtractForm
        self.form = None

        if request.method == 'POST':
            self.method_post()

    def method_post(self):
        self.form = self.editextractform(self.request_post)

        if self.form.is_valid():
            self.insert_by_post()
            # self.transfer_between_accounts()

    def insert_by_post(self):
        if not self.form.cleaned_data['schedule']:
            self.form.save(self.request_user)
            self.transfer_between_accounts()
        else:
            del self.form.cleaned_data['schedule']
            Schedule.objects.create(user_name=self.request_user, **self.form.cleaned_data)
            self.transfer_between_accounts(no_schedule=False)

    def transfer_between_accounts(self, no_schedule=True):
        if self.form.cleaned_data.get('category').startswith('transfer'):
            money_f = self.form.cleaned_data.get('money') * -1
            payment_f = self.form.cleaned_data.get('description')
            description_f = 'credit from ' + self.form.cleaned_data.get('payment')

            if no_schedule:
                self.transfer_in_extract(money_f, description_f, payment_f)
            else:
                self.transfer_by_schedule(money_f, description_f, payment_f)

    def transfer_in_extract(self, money_f, description_f, payment_f):
        Extract.objects.create(
            user_name=self.request_user,
            date=self.form.cleaned_data.get('date'),
            money=money_f,
            description=description_f,
            category=self.form.cleaned_data.get('category'),
            payment=payment_f
        )

    def transfer_by_schedule(self, money_f, description_f, payment_f):
        Schedule.objects.create(
            user_name=self.request_user,
            date=self.form.cleaned_data.get('date'),
            money=money_f,
            description=description_f,
            category=self.form.cleaned_data.get('category'),
            payment=payment_f
        )

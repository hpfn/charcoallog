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
        category = self.form.cleaned_data.get('category')
        schedule = self.form.cleaned_data['schedule']
        del self.form.cleaned_data['schedule']

        if not schedule:
            self.form.save(self.request_user)
        else:
            Schedule.objects.create(user_name=self.request_user, **self.form.cleaned_data)

        if category.startswith('transfer'):
            transfer = TransferBetweenAccounts(self.request_user, self.form)

            if schedule:
                transfer.to_schedule()
            else:
                transfer.to_extract()


class TransferBetweenAccounts:
    def __init__(self, user, form):
        self.data = dict(
            user_name=user,
            date=form.cleaned_data.get('date'),
            money=form.cleaned_data.get('money') * -1,
            category=form.cleaned_data.get('category'),
            description='credit from ' + form.cleaned_data.get('payment'),
            payment=form.cleaned_data.get('description')
        )
        self.category = form.cleaned_data.get('category')

    def to_extract(self):
        Extract.objects.create(**self.data)

    def to_schedule(self):
        Schedule.objects.create(**self.data)

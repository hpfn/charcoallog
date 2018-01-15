from charcoallog.core.models import Extract
from .forms import EditExtractForm


class MethodPost:
    def __init__(self, request_method, request_post, request_user, query_user):
        """
        :param request_method: POST or GET
        :param request_post: dict()
        :param request_user: request.user
        :param query_user: Extract models instance
        """
        # self.request_method = request_method
        self.request_post = request_post
        self.request_user = request_user
        self.query_user = query_user
        self.editextractform = EditExtractForm
        self.form = None

        if request_method == 'POST':
            self.method_post()

    def method_post(self):
        self.form = self.editextractform(self.request_post)
        if self.form.is_valid():
            del self.form.cleaned_data['update_rm']
            del self.form.cleaned_data['pk']
            self.form.cleaned_data['user_name'] = self.request_user

            self.insert_by_post()
            self.transfer_between_accounts()

    def insert_by_post(self):
        self.form.save()

    def transfer_between_accounts(self):
        if self.form.cleaned_data.get('category').startswith('transfer'):
            money_f = self.form.cleaned_data.get('money') * -1
            payment_f = self.form.cleaned_data.get('description')
            description_f = 'credit from ' + self.form.cleaned_data.get('payment')
            Extract.objects.create(
                user_name=self.request_user,
                date=self.form.cleaned_data.get('date'),
                money=money_f,
                description=description_f,
                category=self.form.cleaned_data.get('category'),
                payment=payment_f
            )



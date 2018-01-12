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
            self.insert_by_post()
        else:
            print('INVALID')

    def insert_by_post(self):
        what_to_do = self.form.cleaned_data.get('update_rm')
        del self.form.cleaned_data['update_rm']
        # id_for_update = form.cleaned_data.get('pk')
        del self.form.cleaned_data['pk']

        self.form.cleaned_data['user_name'] = self.request_user

        if not what_to_do:
            self.form.save()
            if self.form.cleaned_data['category'].startswith('transfer'):
                print(self.form.cleaned_data['category'])
                self.transfer_between_accounts()

    def transfer_between_accounts(self):

        money_f = self.form.cleaned_data['money'] * -1
        payment_f = self.form.cleaned_data['description']
        description_f = 'credit to ' + self.form.cleaned_data['description']
        Extract.objects.create(
            user_name=self.request_user,
            date=self.form.cleaned_data['date'],
            money=money_f,
            description=description_f,
            category=self.form.cleaned_data['category'],
            payment=payment_f
        )
        #print(self.form.cleaned_data['payment'])


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
        # elif what_to_do == 'remove':
        #     self.query_user.filter(**form.cleaned_data).delete()
        # elif what_to_do == 'update':
        #     obj = self.query_user.get(id=id_for_update)  # , user_name=self.request_user)
        #     obj.date = form.cleaned_data['date']
        #     obj.money = form.cleaned_data['money']
        #     obj.description = form.cleaned_data['description']
        #     obj.category = form.cleaned_data['category']
        #     obj.payment = form.cleaned_data['payment']
        #     obj.save(update_fields=['date', 'money', 'description', 'category', 'payment'])

    def transfer_between_accounts(self):
        self.form.cleaned_data['money'] = self.form.cleaned_data['money'] * -1
        self.form.cleaned_data['payment'] = self.form.cleaned_data['description']
        self.form.cleaned_data['description'] = 'credit to ' + self.form.cleaned_data['description']
        self.form.save()


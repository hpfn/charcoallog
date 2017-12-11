from .forms import EditExtractForm


class MethodPost:
    def __init__(self, request, query_user):  # , editextractform):
        self.request = request
        self.query_user = query_user
        self.editextractform = EditExtractForm

        self.method_post()

    def method_post(self):
        form = self.editextractform(self.request.POST)

        if form.is_valid():
            self.insert_by_post(form)

    def insert_by_post(self, form):
        what_to_do = form.cleaned_data.get('update_rm')
        del form.cleaned_data['update_rm']
        id_for_update = form.cleaned_data.get('pk')
        del form.cleaned_data['pk']

        form.cleaned_data['user_name'] = self.request.user

        if not what_to_do:
            form.save()
        elif what_to_do == 'remove':
            self.query_user.filter(**form.cleaned_data).delete()
        elif what_to_do == 'update':
            obj = self.query_user.get(id=id_for_update, user_name=self.request.user)
            obj.date = form.cleaned_data['date']
            obj.money = form.cleaned_data['money']
            obj.description = form.cleaned_data['description']
            obj.category = form.cleaned_data['category']
            obj.payment = form.cleaned_data['payment']
            obj.save(update_fields=['date', 'money', 'description', 'category', 'payment'])

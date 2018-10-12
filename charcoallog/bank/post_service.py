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

    def insert_by_post(self):
        transfer = self.form.cleaned_data.get('category').startswith('transfer')
        schedule = self.form.cleaned_data['schedule']
        to_model = 'to_schedule' if schedule else 'to_extract'
        del self.form.cleaned_data['schedule']

        insert_to[to_model](self.request_user, self.form.cleaned_data)

        if transfer:
            data_transfer = build_data_transfer(self.form.cleaned_data)
            insert_to[to_model](self.request_user, data_transfer)


def build_data_transfer(form):
    return dict(
        # user_name=user,
        date=form.get('date'),
        money=form.get('money') * -1,
        category=form.get('category'),
        description='credit from ' + form.get('payment'),
        payment=form.get('description')
    )


def to_extract(user, data):
    Extract.objects.create(user_name=user, **data)


def to_schedule(user, data):
    Schedule.objects.create(user_name=user, **data)


insert_to = dict(
    to_extract=to_extract,
    to_schedule=to_schedule
)

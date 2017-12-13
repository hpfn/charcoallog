from collections import OrderedDict

from .get_service import MethodGet
from .models import Extract
from .post_service import MethodPost


class ShowData:
    """
    :type account_values: dictionary views
          dict.values()
    """
    def __init__(self, request):
        self.request = request
        self.query_user = Extract.objects.user_logged(self.request.user)
        self.account_values = None
        self.form1 = MethodPost(self.request, self.query_user)
        self.form2 = MethodGet(self.request, self.query_user)

    def account_names(self):
        payment_iterator = set(self.query_user.values_list('payment'))

        account = {
            conta[0]: self.query_user.filter(payment=conta[0]).total()
            for conta in payment_iterator
        }

        self.account_values = account.values()

        return OrderedDict(sorted(account.items()))

    def whats_left(self):
        return sum([resto['money__sum'] for resto in self.account_values])


from collections import OrderedDict


class BriefBank:
    """
    :type account_values: dictionary views
          dict.values()
    """
    def __init__(self, query_user):
        self.query_user = query_user
        self.account_values = None

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

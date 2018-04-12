from charcoallog.investments.forms import InvestmentForm


class MethodPost:
    def __init__(self, request, query_user):
        """"
        :param request:
        :param query_user: Investment instance
        """
        # self.request_method = method
        self.request_post = request.POST  # request_post
        # self.request_post['user_name'] = request_user
        # self.request_user = user  # request_user
        self.query_user = query_user
        self.investmentform = InvestmentForm
        self.form = None

        if request.method == 'POST':
            self.request_post['user_name'] = request.user
            self.method_post()

    def method_post(self):
        self.form = self.investmentform(self.request_post)

        if self.form.is_valid():
            self.insert_by_post()

    def insert_by_post(self):
        self.form.save()

from charcoallog.investments.forms import InvestmentForm


class MethodPost:
    def __init__(self, method, data, user, query_user):
        """"
        :param request_method: POST or GET
        :param request_post: dict()
        :param request_user: request.user
        :param query_user: Extract models instance
        """
        # self.request_method = method
        self.request_post = data  # request_post
        self.request_post['user_name'] = user
        # self.request_user = user  # request_user
        self.query_user = query_user
        self.investmentform = InvestmentForm
        self.form = None

        if method == 'POST':
            self.method_post()

    def method_post(self):
        self.form = self.investmentform(self.request_post)

        if self.form.is_valid():
            self.insert_by_post()

    def insert_by_post(self):
        self.form.save()

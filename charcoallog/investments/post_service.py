from charcoallog.investments.forms import InvestmentDetailsForm, InvestmentForm


class MethodPost:
    def __init__(self, request, query_user):
        """"
        :param request:
        :param query_user: Investment instance
        """
        # self.request_method = method
        self.request_post = request.POST  # request_post
        # self.request_post['user_name'] = request_user
        self.request_user = request.user
        self.query_user = query_user
        self.investmentform = InvestmentForm
        self.i_form = None

        self.detailsform = InvestmentDetailsForm
        self.d_form = None

        if request.method == 'POST':
            self.method_post()

    def method_post(self):
        self.i_form = self.investmentform(self.request_post)
        self.d_form = self.detailsform(self.request_post)

        if self.d_form.is_valid():
            self.d_form.save(self.request_user)
        elif self.i_form.is_valid():
            self.i_form.save(self.request_user)

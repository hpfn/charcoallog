from charcoallog.investments.forms import InvestmentDetailsForm


class DetailPost:
    def __init__(self, request):
        self.request = request
        self.i_detail = InvestmentDetailsForm
        self.i_d_form = ''

        if request.method == 'POST':
            self.insert_data()

    def insert_data(self):
        self.i_d_form = self.i_detail(self.request.POST)

        if self.i_d_form.is_valid():
            self.i_d_form.save(self.request.user)

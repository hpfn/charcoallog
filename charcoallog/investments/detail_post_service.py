from charcoallog.investments.forms import BasicDataForm, InvestmentDetailsForm


class DetailPost:
    def __init__(self, request):
        self.request = request
        self.basic_data = BasicDataForm
        self.b_d_form = ''
        self.i_detail = InvestmentDetailsForm
        self.i_d_form = ''

        if request.method == 'POST':
            self.insert_data()

    def insert_data(self):
        self.i_d_form = self.i_detail(self.request.POST)
        self.b_d_form = self.basic_data(self.request.POST)

        if self.i_d_form.is_valid() and self.b_d_form.is_valid():
            basic_data = self.b_d_form.save(self.request.user)
            self.i_d_form.save(basic_data)

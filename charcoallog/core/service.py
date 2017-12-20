from .models import Extract
from .get_service import MethodGet
from .post_service import MethodPost
from .line1_service import Line1


class ShowData:
    def __init__(self, request_method, request_GET, request_POST, request_user):
        #self.request = request
        self.query_user = Extract.objects.user_logged(request_user)
        # self.account_values = None
        self.form1 = MethodPost(request_method, request_POST, request_user, self.query_user)
        self.form2 = MethodGet(request_GET, self.query_user)
        self.line1 = Line1(self.query_user)
        self.account_names = self.line1.account_names()
        self.whats_left = self.line1.whats_left()



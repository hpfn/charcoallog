from charcoallog.core.models import Extract
from charcoallog.core.get_service import MethodGet
from charcoallog.core.post_service import MethodPost
from charcoallog.core.line1_service import Line1


class ShowData:
    def __init__(self, request_method, request_get, request_post, request_user):
        self.query_user = Extract.objects.user_logged(request_user)
        self.form1 = MethodPost(request_method, request_post, request_user, self.query_user)
        self.form2 = MethodGet(request_method, request_get, self.query_user)
        self.line1 = Line1(self.query_user)
        self.account_names = self.line1.account_names()
        self.whats_left = self.line1.whats_left()



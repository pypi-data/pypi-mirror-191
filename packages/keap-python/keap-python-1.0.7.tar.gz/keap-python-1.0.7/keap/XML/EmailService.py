from keap.XML import BaseService


class EmailService(BaseService):
    _service = "APIEmailService"

    def __init__(self, keap):
        super().__init__(keap)

    def get_optin_status(self, email):
        return self.call("getOptStatus", email)

    def optout_email(self, email, reason):
        return self.call("optOut", email)

    def optin_email(self, email, reason):
        return self.call("optIn", email)

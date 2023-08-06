from keap import Keap
from keap.exceptions import KeapUnauthorizedException, KeapException, KeapTokenExpiredException

try:
    from xmlrpclib import ServerProxy, Error
except ImportError:
    from xmlrpc.client import ServerProxy, Error


class BaseService:
    xmlrpc_url = 'https://api.infusionsoft.com/crm/xmlrpc/v1'
    _service = None
    client = None

    def __init__(self, keap: Keap):
        self.keap = keap
        self.get_xmlrpc_client()

    def get_xmlrpc_client(self):
        if not self.keap.token.access_token:
            raise Exception(f"No token set for client {self.keap.app_name}")
        uri = f"{self.xmlrpc_url}?access_token={self.keap.token.access_token}"
        self.client = ServerProxy(uri, use_datetime=self.keap.api_settings.USE_DATETIME,
                                  allow_none=self.keap.api_settings.ALLOW_NONE)
        self.client.error = Error
        return self.client

    def __getattr__(self, method):
        def function(*args):
            return self.call(method, *args)

        return function

    @property
    def service(self):
        return self._service if self._service else self.__class__.__name__

    def call(self, method, *args):
        call = getattr(self.client, f"{self.service}.{method}")
        try:
            return call(self.keap.token.access_token, *args)
        except self.client.error as e:
            error_code = e.errcode
            error_message = e.errmsg
            headers = e.headers
            if error_code == 401:  # Unauthorized
                raise KeapUnauthorizedException(error_message)
            raise KeapException(error_message)

    def server(self):
        return self.client

import json
from datetime import datetime, date
from enum import Enum

import requests

from keap import KeapToken, Keap
from keap.REST.models import BaseDataModel
from keap.exceptions import KeapUnauthorizedException, KeapForbiddenException, KeapTokenExpiredException


class RecordNotFoundError(Exception):
    pass


class BaseService:
    base_api_url = 'https://api.infusionsoft.com/crm/rest/v1'
    api_url: str = None
    _service = None
    client = None
    keap: Keap

    def __init__(self, keap):
        self.keap = keap

    @property
    def token(self) -> KeapToken:
        return self.keap.token

    def _get(self, path: str, params: dict = None):
        return self.restful_request("GET", path, params=params)

    def _post(self, path: str, data: dict = None, params: dict = None):
        return self.restful_request("POST", path, data=data, params=params)

    def _delete(self, path: str, data: dict = None, params: dict = None):
        return self.restful_request("DELETE", path, data=data, params=params)

    def _put(self, path: str, data: dict = None, params: dict = None):
        return self.restful_request("PUT", path, data=data, params=params)

    def _patch(self, path: str, data: dict = None, params: dict = None):
        return self.restful_request("PATCH", path, data=data, params=params)

    def clean_data(self, value):
        if isinstance(value, list):
            for i, v in enumerate(value):
                value[i] = self.clean_data(v)
        if isinstance(value, datetime):
            value = f"{value.strftime('%Y-%m-%d')}T{value.strftime('%H:%M:%S.%f')}Z"
        if isinstance(value, date):
            value = f"{value.strftime('%Y-%m-%d')}"
        if isinstance(value, BaseDataModel):
            value = value.data
        if isinstance(value, Enum):
            value = value.value
        return value

    def serialize(self, data):
        # clean up data dict
        if "self" in data:
            del data['self']
        data = {k: v for k, v in data.items() if v}
        for k, v in data.items():
            data[k] = self.clean_data(v)
        return data

    def restful_request(self, method: str, path: str, data: dict = None, params: dict = None):
        if data is None:
            data = dict()
        if params is None:
            params = dict()
        params["access_token"] = self.token.access_token
        headers = {
            'Content-Type': 'application/json'
        }

        # clean up data
        data = self.serialize(data)
        params = self.serialize(params)

        url = f"{self.base_api_url}/{path}"
        if method.lower() in ['get', 'delete']:
            response = requests.request(method, url, headers=headers, params=params)
        else:
            response = requests.request(method, url, headers=headers, data=json.dumps(data), params=params)

        # TODO: Implement rate limiting here. response.headers contains the Apigee rate limiting info.
        if response.status_code == 204:  # No Content
            return True
        response_json = response.json()
        if type(response_json) is list:
            return response_json
        fault = response_json.get('fault', {}).get('faultstring', 'Error')
        if response.status_code == 401:  # Unauthorized
            raise KeapUnauthorizedException(fault)
        if response.status_code == 403:  # Forbidden
            raise KeapForbiddenException(fault)
        if response.status_code == 404:  # Not Found
            raise RecordNotFoundError(fault)

        return response_json

    @property
    def service(self):
        return self._service if self._service else self.__class__.__name__

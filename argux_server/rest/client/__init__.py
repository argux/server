"""Argux REST client for Argux Server."""

import json
import requests

import logging

from requests.exceptions import (
    ConnectionError,
    HTTPError
)

from argux_server.util import (
    DATE_FMT
)


class AbstractRESTClient:

    """RESTClient.

    Class used to interact with ArguxServer
    """

    logger = logging.getLogger(__name__)

    def __init__(self, base_url, username, secret):
        """Initialise RESTClient.

        Arguments:
            base_url:   base-url of argux-server, eg:
                        https://argux-server:port/
        """
        self.base_url = base_url
        self.username = username
        self.secret = secret
        self.cookies = {}
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

    # pylint: disable=no-self-use
    def __check_status_code(self, response):
        if response.status_code not in (
                requests.codes.ok,
                requests.codes.created):
            response.raise_for_status()

    def login(self):
        payload = {
            'username': self.username,
            'password': self.secret
        }
        try:
            response = requests.post(
                self.base_url+'/rest/1.0/login',
                headers=self.headers,
                data=json.dumps(payload))

            self.__check_status_code(response)

            self.cookies['argux_server'] = response.cookies['argux_server']
            self.headers['X-Csrf-token'] = response.headers['X-Csrf-token']
        except ConnectionError as err:
            print(err)

    def get(self, path):
        try:
            response = requests.get(
                self.base_url + path,
                cookies=self.cookies,
                headers=self.headers)

            self.__check_status_code(response)

            # Check if a new cookie is provided.
            if 'argux_server' in response.cookies:
                self.cookies['argux_server'] = response.cookies['argux_server']
        except ConnectionError as err:
            raise err
        except HTTPError as err:
            raise err

        return response

    def post(self, path, data):
        try:
            response = requests.post(
                self.base_url + path,
                data=data,
                cookies=self.cookies,
                headers=self.headers)

            self.__check_status_code(response)

            # Check if a new cookie is provided.
            if 'argux_server' in response.cookies:
                self.cookies['argux_server'] = response.cookies['argux_server']
        except ConnectionError as err:
            raise err
        except HTTPError as err:
            raise err

        return response

    def delete(self, path):
        try:
            response = requests.delete(
                self.base_url + path,
                cookies=self.cookies,
                headers=self.headers)

            self.__check_status_code(response)

            # Check if a new cookie is provided.
            if 'argux_server' in response.cookies:
                self.cookies['argux_server'] = response.cookies['argux_server']
        except ConnectionError as err:
            raise err
        except HTTPError as err:
            raise err

        return response


class RESTClient(AbstractRESTClient):

    def create_item(self, host, key, params):

        payload = {
            'name': params['name'],
            'description': params['description'],
            'category': params['category'],
            'type': params['type'],
            'unit': params['unit'],
        }

        try:
            response = self.post(
                '/rest/1.0/host/'+host+'/item/'+key,
                data=json.dumps(payload))
        except ConnectionError as err:
            raise err
        except HTTPError as err:
            raise err

        return response

    def push_value(self, host, key, timestamp, value):

        payload = {
            'value': value,
            'timestamp': timestamp.strftime(DATE_FMT)
        }

        try:
            response = self.post(
                '/rest/1.0/host/'+host+'/item/'+key+'/values',
                data=json.dumps(payload))
        except ConnectionError as err:
            raise err
        except HTTPError as err:
            raise err

        return response

    def get_monitors(self, monitor_type):
        try:
            response = self.get('/rest/1.0/monitor/'+monitor_type)
        except ConnectionError as err:
            raise err
        except HTTPError as err:
            raise err

        try:
            json_response = response.json()
        except Exception as err:
            print("\""+str(response)+"\"")
            raise ValueError(
                'Invalid Response, could not decode JSON')

        if json_response is None:
            raise ValueError(
                'Invalid Response, could not decode JSON')
        if 'monitors' not in json_response:
            raise ValueError(
                'Invalid Response, missing \'monitors\' attribute')

        return json_response['monitors']

    def get_dns_domains(self, host, address):

        try:
            response = self.get(
                '/rest/1.0/monitor/dns/'+host+'/'+address+'/domain')
        except ConnectionError as err:
            raise err
        except HTTPError as err:
            raise err

        json_response = response.json()
        if json_response is None:
            raise ValueError(
                'Invalid Response, could not decode JSON')
        if 'domains' not in json_response:
            raise ValueError(
                'Invalid Response, missing \'domains\' attribute')

        return json_response['domains']

    def evaluate_triggers(self):

        try:
            response = self.post(
                '/rest/1.0/monitor/trigger/evaluate',
                data='')
        except ConnectionError as err:
            raise err
        except HTTPError as err:
            self.logger.error("HttpError:"+ str(err))

        return response

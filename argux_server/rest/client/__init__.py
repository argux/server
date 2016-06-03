"""Argux REST client for Argux Server."""

import json
import requests

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

            self.cookies['argux_server'] = response.cookies['argux_server']
            self.headers['X-Csrf-token'] = response.headers['X-Csrf-token']
        except ConnectionError as e:
            print(e)

    def get(self, path):
        try:
            response = requests.get(
                self.base_url + path,
                cookies = self.cookies,
                headers = self.headers)

            # Check if a new cookie is provided.
            if 'argux_server' in response.cookies:
                self.cookies['argux_server'] = response.cookies['argux_server']
        except ConnectionError as e:
            raise e
        except HTTPError as e:
            raise e

        return response

    def post(self, path, data):
        try:
            response = requests.post(
                self.base_url + path,
                data = data,
                cookies = self.cookies,
                headers = self.headers)

            # Check if a new cookie is provided.
            if 'argux_server' in response.cookies:
                self.cookies['argux_server'] = response.cookies['argux_server']
        except ConnectionError as e:
            raise e
        except HTTPError as e:
            raise e

        return response

    def delete(self, path):
        try:
            response = requests.delete(
                self.base_url + path,
                cookies = self.cookies,
                headers = self.headers)

            # Check if a new cookie is provided.
            if 'argux_server' in response.cookies:
                self.cookies['argux_server'] = response.cookies['argux_server']
        except ConnectionError as e:
            raise e
        except HTTPError as e:
            raise e

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
        except ConnectionError as e:
            raise e
        except HTTPError as e:
            raise e 

        return []

    def push_value(self, host, key, timestamp, value):

        payload = {
            'value': value,
            'timestamp': timestamp.strftime(DATE_FMT)
        }

        try:
            response = self.post(
                '/rest/1.0/host/'+host+'/item/'+key+'/values',
                data=json.dumps(payload))
        except ConnectionError as e:
            raise e
        except HTTPError as e:
            raise e 

        return []

    def get_monitors(self, monitor_type):
        try:
            response = self.get('/rest/1.0/monitor/'+monitor_type)
        except ConnectionError as e:
            raise e
        except HTTPError as e:
            raise e

        try:
            json_response = response.json()
        except Exception as e:
            print("\""+str(response)+"\"")
            raise ValueError('Invalid Response, could not decode JSON')

        if json_response is None:
            raise ValueError('Invalid Response, could not decode JSON')
        if not 'monitors' in json_response:
            raise ValueError('Invalid Response, missing \'monitors\' attribute')

        return json_response['monitors']


    def get_dns_domains(self, host, address):

        try:
            response = self.get(
                '/rest/1.0/monitor/dns/'+host+'/'+address+'/domain')
        except ConnectionError as e:
            raise e
        except HTTPError as e:
            raise e 

        json_response = response.json()
        if json_response is None:
            raise ValueError('Invalid Response, could not decode JSON')
        if not 'domains' in json_response:
            raise ValueError('Invalid Response, missing \'domains\' attribute')

        return json_response['domains']

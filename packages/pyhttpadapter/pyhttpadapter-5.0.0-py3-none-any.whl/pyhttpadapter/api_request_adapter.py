# imports
import sys
import os
import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import ConnectionError, SSLError
import json

sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from adp_config import RETRIES, TIMEOUT


class CustomAdapter:
    """HTTP Adapter class for calling 3rd party api"""

    def __init__(
        self,
        method,
        url,
        auth_type,
        payload=None,
        headers=None,
        username=None,
        password=None,
        token=None,
        ssl_cert=None,
    ):
        """Init method to define constructor arguments"""
        self.method = method
        self.url = url
        self.payload = payload
        self.headers = headers
        self.auth_type = auth_type
        self.username = username
        self.password = password
        self.token = token
        self.ssl_cert_path = ssl_cert

    def run(self):
        """Method to call 3rd party api"""

        if self.ssl_cert_path:
            ssl_cert_path = self.ssl_cert_path
        else:
            ssl_cert_path = False

        if self.headers:
            headers = json.loads(self.headers)
        else:
            headers = {}

        if self.payload:
            payload = json.loads(self.payload)
        else:
            payload = {}

        if self.auth_type.lower() == "basic auth":
            # Api calling with basic authentication

            try:
                # api retry code. It will retry max 3 times as
                # # defined in adp_config.py configuration file
                s = requests.Session()
                retries = Retry(total=RETRIES, backoff_factor=0.1, status_forcelist=[502, 503, 504])

                s.mount("https://", HTTPAdapter(max_retries=retries))
                s.mount("http://", HTTPAdapter(max_retries=retries))

                response = s.request(
                    self.method,
                    self.url,
                    headers=headers,
                    data=payload,
                    auth=HTTPBasicAuth(self.username, self.password),
                    verify=ssl_cert_path,
                    timeout=TIMEOUT,
                )
            except ConnectionError as cre:
                response = requests.models.Response()
                response.status_code = 504
                response._content = "No Response".encode("utf-8")
                response.encoding = "utf-8"
                return response

            except SSLError as se:
                response = requests.models.Response()
                response.status_code = 400
                response._content = "Invalid SSL Certificate".encode("utf-8")
                response.encoding = "utf-8"
                return response

        elif self.auth_type.lower() == "bearer token auth":
            # Api calling with bearer token authentication

            headers.update({"Authorization": "Bearer " + self.token})
            try:
                s = requests.Session()

                retries = Retry(total=RETRIES, backoff_factor=0.1, status_forcelist=[502, 503, 504])

                s.mount("https://", HTTPAdapter(max_retries=retries))
                s.mount("http://", HTTPAdapter(max_retries=retries))

                response = s.request(
                    self.method,
                    self.url,
                    headers=headers,
                    data=payload,
                    verify=ssl_cert_path,
                    timeout=TIMEOUT,
                )
            except ConnectionError as cre:
                response = requests.models.Response()
                response.status_code = 504
                response._content = "No Response".encode("utf-8")
                response.encoding = "utf-8"
                return response
            except SSLError as se:
                response = requests.models.Response()
                response.status_code = 400
                response._content = "Invalid SSL Certificate".encode("utf-8")
                response.encoding = "utf-8"
                return response

        elif self.auth_type.lower() == "no auth":
            # Api calling without any authentication

            try:
                s = requests.Session()

                retries = Retry(total=RETRIES, backoff_factor=0.1, status_forcelist=[502, 503, 504])

                s.mount("https://", HTTPAdapter(max_retries=retries))
                s.mount("http://", HTTPAdapter(max_retries=retries))

                response = s.request(
                    self.method,
                    self.url,
                    headers=headers,
                    data=payload,
                    verify=ssl_cert_path,
                    timeout=TIMEOUT,
                )

            except ConnectionError as cre:
                response = requests.models.Response()
                response.status_code = 504
                response._content = "No Response".encode("utf-8")
                response.encoding = "utf-8"
                return response
            except SSLError as se:
                response = requests.models.Response()
                response.status_code = 400
                response._content = "Invalid SSL Certificate".encode("utf-8")
                response.encoding = "utf-8"
                return response

        else:
            response = {"message": "Please provide authorization type 1. Basic Auth 2. Bearer Token Auth 3. No Auth"}
            return response

        return response

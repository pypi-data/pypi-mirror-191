# imports
import requests
import json
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter, Retry
from requests.exceptions import ConnectionError, SSLError
import urllib.parse
import yaml
import os

config_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),'adap_config.yaml')

class CustomAdapter:
    """HTTP Adapter class for calling 3rd party api"""


    # Opening a config file using yaml
    with open(config_file_path,"rb") as file:
        config_data = yaml.load(file, Loader=yaml.FullLoader)
  

    def __init__(
        self,
        method,
        url,
        payload=None,
        auth_type=None,
        headers=None,
        username=None,
        password=None,
        token=None,
        ssl_cert_path=None,
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
        self.ssl_cert_path = ssl_cert_path

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

        o = urllib.parse.urlsplit(self.url)

        # check url proctocol and  ask to verify SSL certificate if needed
        if o.scheme == "https" and ssl_cert_path == False:
            response = requests.models.Response()
            response._content = "Unverified HTTPS Request. Please provide SSL certificate for verification".encode(
                "utf-8"
            )
            response.encoding = "utf-8"
            return response.text

        if self.auth_type.lower() == "basic auth":
            # Api calling with basic authentication

            try:
                # api retry code. It will retry max 3 times as defined in adp_config.py configuration file
                s = requests.Session()
                retries = Retry(
                    total=self.config_data['RETRIES'], backoff_factor=0.1, status_forcelist=[502, 503, 504]
                )

                s.mount("https://", HTTPAdapter(max_retries=retries))
                s.mount("http://", HTTPAdapter(max_retries=retries))

                response = s.request(
                    self.method,
                    self.url,
                    headers=headers,
                    data=payload,
                    auth=HTTPBasicAuth(self.username, self.password),
                    verify=ssl_cert_path,
                    timeout=self.config_data['TIMEOUT'],
                )
            except ConnectionError as cre:
                response = requests.models.Response()
                response.status_code = 504
                response._content = "No Response".encode("utf-8")
                response.encoding = "utf-8"
                return response.text

            except SSLError as se:
                response = requests.models.Response()
                response.status_code = 400
                response._content = "Invalid SSL Certificate".encode("utf-8")
                response.encoding = "utf-8"
                return response.text

        elif self.auth_type.lower() == "bearer token auth":
            # Api calling with bearer token authentication

            headers.update({"Authorization": "Bearer " + self.token})
            try:
                s = requests.Session()

                retries = Retry(
                    total=self.config_data['RETRIES'], backoff_factor=0.1, status_forcelist=[502, 503, 504]
                )

                s.mount("https://", HTTPAdapter(max_retries=retries))
                s.mount("http://", HTTPAdapter(max_retries=retries))

                response = s.request(
                    self.method,
                    self.url,
                    headers=headers,
                    data=payload,
                    verify=ssl_cert_path,
                    timeout=self.config_data['TIMEOUT'],
                )
            except ConnectionError as cre:
                response = requests.models.Response()
                response.status_code = 504
                response._content = "No Response".encode("utf-8")
                response.encoding = "utf-8"
                return response.text
            except SSLError as se:
                response = requests.models.Response()
                response.status_code = 400
                response._content = "Invalid SSL Certificate".encode("utf-8")
                response.encoding = "utf-8"
                return response.text

        elif self.auth_type.lower() == "no auth":
            # Api calling without any authentication

            try:
                s = requests.Session()

                retries = Retry(
                    total=self.config_data['RETRIES'], backoff_factor=0.1, status_forcelist=[502, 503, 504]
                )

                s.mount("https://", HTTPAdapter(max_retries=retries))
                s.mount("http://", HTTPAdapter(max_retries=retries))

                response = s.request(
                    self.method,
                    self.url,
                    headers=headers,
                    data=payload,
                    verify=ssl_cert_path,
                    timeout=self.config_data['TIMEOUT'],
                )

            except ConnectionError as cre:
                response = requests.models.Response()
                response.status_code = 504
                response._content = "No Response".encode("utf-8")
                response.encoding = "utf-8"
                return response.text
            except SSLError as se:
                response = requests.models.Response()
                response.status_code = 400
                response._content = "Invalid SSL Certificate".encode("utf-8")
                response.encoding = "utf-8"
                return response.text

        else:
            response = {"message": "Please provide authorization type"}
            return response

        return response


if __name__ == "__main__":
    method = input("API Method: ")
    url = input("API URL: ")
    payload = input("API Payload in Json Format: ")
    auth_type = input("Authorization Type: ")
    headers = input("API headers: ")
    username = input("Auth Username: ")
    password = input("Auth Password: ")
    token = input("Bearer Token: ")
    ssl_cert = input("SSL Certificate path: ")

    ca = CustomAdapter(
        method, url, payload, auth_type, headers, username, password, token, ssl_cert
    )
    data = ca.run()
    print(data)

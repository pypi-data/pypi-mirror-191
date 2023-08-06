# sac_httpadaptor_kd
Python based HTTP adaptor.

## Project description

The HTTP Adapter can be used to call any REST or 3rd party API's available over internet. supporting both HTTP and HTTPS protocol.

This module allows to perform any HTTP request like GET,POST,PUT,PATCH,DELETE to 3rd party API's





## Installation

Using Python package manager you can install this module by using below command:

pip install pyhttpadapter

```bash
  pip install pyhttpadapter
```
    
## Usage/Examples

Class CustomAdapter takes number of arguments as shown below. If not provided keep it blank.

CustomAdapter(method, url, payload, auth_type, headers, username, password, token, ssl_cert_path)

User need to provide value for auth_type out of below 3 options without fail:
1) Basic Auth
2) Bearer Token Auth
3) No auth



#imports
from pyhttpadapter.api_request_adapter import CustomAdapter

obj = CustomAdapter(method='GET' , url='https://gorest.co.in/public/v2/users', auth_type='no auth')

response = obj.run()

print(response.json())

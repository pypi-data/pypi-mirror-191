#create
import requests


class Request:
    def __init__(self, url, Auth_Token, payload, req):
        self.headers= {
                        'Authorization': 'Bearer ' + Auth_Token,
                        'Content-Type': 'application/json',
                        }
        self.response = requests.request(req, url, headers=self.headers, data=payload)


import requests
class ApiClient:
    BASE_URL = "https://petstore.swagger.io/v2"

    def __init__(self):
        self.session = requests.Session()

    def get(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.get(url, params=params)
        return response

    def post(self, endpoint, data=None, json=None, files=None):
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.post(url, data=data, json=json, files=files)
        return response

    def put(self, endpoint, data=None, json=None):
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.put(url, data=data, json=json)
        return response

    def delete(self, endpoint, params=None):
        url = f"{self.BASE_URL}{endpoint}"
        response = self.session.delete(url, params=params)
        return response
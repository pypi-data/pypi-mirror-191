import requests


class IPMike:
    def __init__(self):
        self.url = "https://ipmike.com/iplocation"
        self.token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"

    def get_location(self, ip):
        params = {"token": self.token, "ip": ip}
        response = requests.get(self.url, params=params)
        return response.json()

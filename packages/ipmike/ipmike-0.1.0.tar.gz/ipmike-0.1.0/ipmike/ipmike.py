import requests

def get_location(ip):
    url = "https://ipmike.com/iplocation"
    params = {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9",
        "ip": ip
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Request failed with status code: {}".format(response.status_code))
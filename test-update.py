import requests

BASE = " http://127.0.0.1:5000/"
APP_VERSION = "v1/"

response = requests.patch(BASE + APP_VERSION + "video/2", {"likes":10077})
print(response.json())
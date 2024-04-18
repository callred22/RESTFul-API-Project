import requests

BASE = " http://127.0.0.1:5000/"
APP_VERSION = "v1/"

data = [{"likes": 78, 'name': "The Frozen Ones", 'views': 100},
        {"likes": 2078, 'name': "The Frozen Void", 'views': 1020},
        {"likes": 178, 'name': "The Mars Experiment", 'views': 10}]
for i in range(len(data)):
    response = requests.put(BASE + APP_VERSION + "video/" + str(i), data[i])
    print(response.json())

input()
response = requests.get(BASE + APP_VERSION + "video/2")
print(response.json())
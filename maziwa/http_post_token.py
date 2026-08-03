import requests

url='http://127.0.0.1:8000/api/token/'
resp = requests.post(url, json={'username':'truck_a','password':'truck123'})
print('STATUS', resp.status_code)
print(resp.text[:5000])

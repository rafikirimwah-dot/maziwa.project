import urllib.request, json

url = 'http://127.0.0.1:8000/api/token/'
data = json.dumps({'username':'truck_a','password':'truck123'}).encode('utf-8')
req = urllib.request.Request(url, data=data, headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req) as resp:
        print('STATUS', resp.status)
        print(resp.read().decode('utf-8')[:8000])
except Exception as e:
    # Attempt to read the response body from the exception if available
    try:
        body = e.read().decode('utf-8')
        print('ERROR RESPONSE BODY:\n', body[:8000])
    except Exception:
        print('EXCEPTION', type(e), e)

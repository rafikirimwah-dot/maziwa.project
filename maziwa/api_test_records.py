import urllib.request, json

def post_token(username, password):
    url='http://127.0.0.1:8000/api/token/'
    data = json.dumps({'username':username,'password':password}).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def get_records(token):
    url='http://127.0.0.1:8000/api/milk-records/'
    req = urllib.request.Request(url, headers={'Authorization': f'Bearer {token}'})
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)

if __name__=='__main__':
    t = post_token('truck_a','truck123')
    print('TOKEN OK')
    records = get_records(t['access'])
    print('RECORDS COUNT', len(records))
    print(records[:2])

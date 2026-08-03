import sys
import json
import urllib.request
import urllib.parse

TOKEN_URL = "http://127.0.0.1:8000/api/token/"
RECORDS_URL = "http://127.0.0.1:8000/api/milk-records/"

creds = {"username": "truck_a", "password": "truck123"}

data = urllib.parse.urlencode(creds).encode()
req = urllib.request.Request(TOKEN_URL, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        token_body = resp.read().decode()
        status = resp.getcode()
except Exception as e:
    print("ERROR: token request failed:", e)
    sys.exit(2)

print("TOKEN status:", status)
try:
    token_json = json.loads(token_body)
    print(json.dumps(token_json, indent=2))
except Exception:
    print(token_body)

if status != 200:
    sys.exit(3)

access = token_json.get("access")
if not access:
    print("No access token in response")
    sys.exit(4)

headers = {"Authorization": f"Bearer {access}"}
req2 = urllib.request.Request(RECORDS_URL, headers=headers)
try:
    with urllib.request.urlopen(req2, timeout=10) as resp2:
        records_body = resp2.read().decode()
        status2 = resp2.getcode()
except Exception as e:
    print("ERROR: records request failed:", e)
    sys.exit(5)

print("RECORDS status:", status2)
try:
    print(json.dumps(json.loads(records_body), indent=2))
except Exception:
    print(records_body)

sys.exit(0)

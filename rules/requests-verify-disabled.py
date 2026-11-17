import requests

# ruleid: requests-verify-disabled
requests.get("https://example.com", verify=False)

# ruleid: requests-verify-disabled
requests.post("https://example.com", json={}, verify=False, timeout=5)

s = requests.Session()
# ruleid: requests-verify-disabled
s.verify = False

# ruleid: requests-verify-disabled
s.get("https://example.com", verify=False)

# ok: requests-verify-disabled
requests.get("https://example.com", timeout=5)

# ok: requests-verify-disabled
requests.get("https://internal.example", verify="/etc/ssl/internal-ca.pem")

import requests

# ruleid: requests-no-verify
requests.get("https://example.com", verify=False)

# ok: requests-no-verify
requests.get("https://example.com")

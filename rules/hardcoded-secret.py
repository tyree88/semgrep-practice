import os
from flask import Flask

app = Flask(__name__)

# ruleid: hardcoded-secret
app.config["SECRET_KEY"] = "changeme"

# ok: hardcoded-secret
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

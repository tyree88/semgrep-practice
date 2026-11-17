import os
from flask import Flask

app = Flask(__name__)

# ruleid: hardcoded-secret-key
app.config["SECRET_KEY"] = "changeme"

# ruleid: hardcoded-secret-key
app.secret_key = "changeme"

# ruleid: hardcoded-secret-key
app.config.update(DEBUG=False, SECRET_KEY="changeme")

# ruleid: hardcoded-secret-key
app.config.update({"SECRET_KEY": "changeme"})

# ruleid: hardcoded-secret-key
app.config.from_mapping(SECRET_KEY="changeme")

# ok: hardcoded-secret-key
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

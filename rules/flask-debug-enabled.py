import os
from flask import Flask

app = Flask(__name__)

# ruleid: flask-debug-enabled
app.run(debug=True)

# ruleid: flask-debug-enabled
app.run("0.0.0.0", 8080, debug=True)

# ok: flask-debug-enabled
app.run(debug=os.environ.get("FLASK_DEBUG") == "1")

# ok: flask-debug-enabled
app.run()

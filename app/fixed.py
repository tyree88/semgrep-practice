"""Fixed twin of app/vulnerable.py. Custom rules in rules/ should report nothing here."""
import ast
import hashlib
import ipaddress
import json
import os
import sqlite3
import subprocess

import requests
import yaml
from flask import Flask, abort, request
from werkzeug.utils import safe_join

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or os.urandom(32)

FILES_DIR = os.path.join(os.path.dirname(__file__), "files")
ALLOWED_URLS = {"status": "https://www.githubstatus.com/api/v2/status.json"}


def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (name TEXT, role TEXT)")
    conn.executemany("INSERT INTO users VALUES (?, ?)", [("alice", "admin"), ("bob", "user")])
    return conn


@app.route("/user")
def user():
    name = request.args.get("name", "")
    rows = get_db().execute("SELECT name, role FROM users WHERE name = ?", (name,)).fetchall()
    return {"rows": rows}


@app.route("/ping")
def ping():
    try:
        host = str(ipaddress.ip_address(request.args.get("host", "127.0.0.1")))
    except ValueError:
        abort(400)
    out = subprocess.run(["ping", "-c", "1", host], capture_output=True, text=True)
    return out.stdout

@app.route("/file")
def read_file():
    path = safe_join(FILES_DIR, request.args.get("name", "readme.txt"))
    if path is None or not os.path.isfile(path):
        abort(404)
    with open(path) as f:
        return f.read()


@app.route("/fetch")
def fetch():
    key = request.args.get("key", "")
    if key not in ALLOWED_URLS:
        abort(400)
    return requests.get(ALLOWED_URLS[key], timeout=5).text


@app.route("/calc")
def calc():
    try:
        return str(ast.literal_eval(request.args.get("expr", "1")))
    except (ValueError, SyntaxError):
        abort(400)


@app.route("/load", methods=["POST"])
def load():
    try:
        return str(json.loads(request.get_data()))
    except ValueError:
        abort(400)


@app.route("/config", methods=["POST"])
def config():
    try:
        return str(yaml.safe_load(request.get_data()))
    except yaml.YAMLError:
        abort(400)


@app.route("/hash")
def hash_password():
    pw = request.args.get("pw", "")
    salt = os.urandom(16)
    return salt.hex() + ":" + hashlib.scrypt(pw.encode(), salt=salt, n=2**14, r=8, p=1).hex()


if __name__ == "__main__":
    app.run(debug=os.environ.get("FLASK_DEBUG") == "1")

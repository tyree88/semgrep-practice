"""INTENTIONALLY VULNERABLE Flask app for SAST practice. NEVER deploy or expose this.

Every route has a twin in app/fixed.py. Your custom rules in rules/ should
flag this file and stay quiet on fixed.py.
"""
import hashlib
import os
import pickle
import sqlite3
import subprocess

import requests
import yaml
from flask import Flask, request

app = Flask(__name__)
app.config["SECRET_KEY"] = "dev-only-not-a-real-secret"  # hardcoded-secret-key

FILES_DIR = os.path.join(os.path.dirname(__file__), "files")


def get_db():
    conn = sqlite3.connect(":memory:")
    conn.execute("CREATE TABLE users (name TEXT, role TEXT)")
    conn.executemany("INSERT INTO users VALUES (?, ?)", [("alice", "admin"), ("bob", "user")])
    return conn


@app.route("/user")
def user():
    name = request.args.get("name", "")
    query = f"SELECT name, role FROM users WHERE name = '{name}'"  # flask-sqli
    return {"rows": get_db().execute(query).fetchall()}


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    out = subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True)  # flask-command-injection
    return out.stdout


@app.route("/file")
def read_file():
    name = request.args.get("name", "readme.txt")
    with open(os.path.join(FILES_DIR, name)) as f:  # flask-path-traversal
        return f.read()


@app.route("/fetch")
def fetch():
    url = request.args.get("url", "")
    return requests.get(url, verify=False).text  # flask-ssrf, requests-verify-disabled


@app.route("/calc")
def calc():
    expr = request.args.get("expr", "1+1")
    return str(eval(expr))  # flask-code-injection


@app.route("/load", methods=["POST"])
def load():
    return str(pickle.loads(request.get_data()))  # insecure-deserialization


@app.route("/config", methods=["POST"])
def config():
    return str(yaml.load(request.get_data(), Loader=yaml.Loader))  # insecure-deserialization


@app.route("/hash")
def hash_password():
    pw = request.args.get("pw", "")
    return hashlib.md5(pw.encode()).hexdigest()  # weak-hash


if __name__ == "__main__":
    app.run(debug=True)  # flask-debug-enabled

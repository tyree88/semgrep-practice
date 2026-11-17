"""A tiny Flask app with 4 security bugs ON PURPOSE. Never deploy it.

Each bug has a matching rule in rules/. Run: uvx semgrep scan --config rules/ app.py
"""
import sqlite3
import subprocess

import requests
from flask import Flask, request

app = Flask(__name__)

# Bug 1 (rules/hardcoded-secret.yaml): the secret is written in the code.
app.config["SECRET_KEY"] = "dev-only-not-a-real-secret"


@app.route("/user")
def user():
    name = request.args.get("name", "")
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE users (name TEXT)")
    # Bug 2 (rules/sql-injection.yaml): user input is pasted into the SQL text.
    # Try /user?name=' OR '1'='1
    return {"rows": db.execute(f"SELECT * FROM users WHERE name = '{name}'").fetchall()}


@app.route("/ping")
def ping():
    host = request.args.get("host", "127.0.0.1")
    # Bug 3 (rules/command-injection.yaml): shell=True runs the input as a shell command.
    # Try /ping?host=127.0.0.1;whoami
    return subprocess.run(f"ping -c 1 {host}", shell=True, capture_output=True, text=True).stdout


@app.route("/status")
def status():
    # Bug 4 (rules/requests-no-verify.yaml): verify=False turns off HTTPS certificate checks.
    return requests.get("https://www.githubstatus.com/api/v2/status.json", verify=False).text

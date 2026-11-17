import sqlite3
from flask import request

db = sqlite3.connect(":memory:")


def bad():
    name = request.args.get("name")
    # ruleid: sql-injection
    db.execute(f"SELECT * FROM users WHERE name = '{name}'")


def good():
    name = request.args.get("name")
    # ok: sql-injection
    db.execute("SELECT * FROM users WHERE name = ?", (name,))

import sqlite3
from flask import request

conn = sqlite3.connect(":memory:")


def bad_fstring():
    name = request.args.get("name")
    # ruleid: flask-sqli
    conn.execute(f"SELECT * FROM users WHERE name = '{name}'")


def bad_concat():
    # ruleid: flask-sqli
    conn.cursor().execute("SELECT * FROM users WHERE id = " + request.form["id"])


def bad_via_variable():
    query = "DELETE FROM users WHERE name = '%s'" % request.args["name"]
    # ruleid: flask-sqli
    conn.executescript(query)


def ok_parameterized():
    name = request.args.get("name")
    # ok: flask-sqli
    conn.execute("SELECT * FROM users WHERE name = ?", (name,))


def ok_constant():
    # ok: flask-sqli
    conn.execute("SELECT count(*) FROM users")

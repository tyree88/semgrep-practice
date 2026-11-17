import os
from flask import request, send_file
from werkzeug.utils import safe_join

BASE = "/srv/files"


def bad_join():
    name = request.args.get("name")
    # ruleid: flask-path-traversal
    return open(os.path.join(BASE, name)).read()


def bad_send_file():
    # ruleid: flask-path-traversal
    return send_file(BASE + "/" + request.args["name"])


def ok_safe_join():
    path = safe_join(BASE, request.args.get("name"))
    if path is None:
        return "no", 404
    # ok: flask-path-traversal
    return open(path).read()

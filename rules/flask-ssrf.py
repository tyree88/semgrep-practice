import urllib.request
import requests
from flask import request

ALLOWED = {"status": "https://example.com/status"}


def bad_urlopen():
    # ruleid: flask-ssrf
    return urllib.request.urlopen(request.args["url"]).read()


def bad_requests():
    url = "http://" + request.args.get("host") + "/admin"
    # ruleid: flask-ssrf
    return requests.get(url).text


def ok_allowlist():
    key = request.args.get("key")
    if key not in ALLOWED:
        return "no", 400
    # ok: flask-ssrf
    return urllib.request.urlopen(ALLOWED[key]).read()


LOOKUP = {"status": "https://example.com/status"}


def bad_not_an_allowlist():
    # ruleid: flask-ssrf
    return urllib.request.urlopen(LOOKUP[request.args["key"]]).read()


def bad_requests_request():
    # ruleid: flask-ssrf
    return requests.request("GET", request.args["u"]).text


def bad_url_keyword():
    # ruleid: flask-ssrf
    return requests.get(url=request.args["u"]).text


def ok_tainted_method_only():
    # ok: flask-ssrf
    return requests.request(request.args["m"], "https://example.com").text

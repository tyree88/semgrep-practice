"""Behavior tests: the fixed app must actually block the attacks, not just pass Semgrep."""
from app.fixed import app

client = app.test_client()


def test_sqli_payload_returns_nothing():
    assert client.get("/user", query_string={"name": "' OR '1'='1"}).json["rows"] == []
    assert client.get("/user", query_string={"name": "alice"}).json["rows"] == [["alice", "admin"]]


def test_path_traversal_blocked():
    assert client.get("/file", query_string={"name": "../fixed.py"}).status_code == 404
    assert client.get("/file", query_string={"name": "readme.txt"}).status_code == 200


def test_command_injection_rejected():
    assert client.get("/ping", query_string={"host": "127.0.0.1; id"}).status_code == 400


def test_ssrf_unknown_key_rejected():
    assert client.get("/fetch", query_string={"key": "http://169.254.169.254/"}).status_code == 400


def test_calc_rejects_code():
    assert client.get("/calc", query_string={"expr": "__import__('os').getcwd()"}).status_code == 400
    assert client.get("/calc", query_string={"expr": "[1, 2]"}).data == b"[1, 2]"


def test_yaml_rejects_python_tags():
    assert client.post("/config", data="!!python/object/apply:os.getcwd []").status_code == 400

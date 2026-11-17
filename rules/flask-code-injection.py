import ast
from flask import request


def bad_eval():
    # ruleid: flask-code-injection
    return eval(request.args.get("expr"))


def bad_exec():
    code = "x = " + request.form["value"]
    # ruleid: flask-code-injection
    exec(code)


def ok_literal_eval():
    # ok: flask-code-injection
    return ast.literal_eval(request.args.get("expr"))


def ok_constant():
    # ok: flask-code-injection
    return eval("1 + 1")

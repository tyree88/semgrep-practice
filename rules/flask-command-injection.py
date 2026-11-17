import os
import subprocess
from flask import request


def bad_shell_true():
    host = request.args.get("host")
    # ruleid: flask-command-injection
    subprocess.run(f"ping -c 1 {host}", shell=True)


def bad_os_system():
    # ruleid: flask-command-injection
    os.system("nslookup " + request.args["domain"])


def ok_arg_list():
    host = request.args.get("host")
    # ok: flask-command-injection
    subprocess.run(["ping", "-c", "1", host])


def ok_constant_shell():
    # ok: flask-command-injection
    subprocess.run("uptime", shell=True)

import subprocess

host = input()

# ruleid: command-injection
subprocess.run(f"ping -c 1 {host}", shell=True)

# ok: command-injection
subprocess.run(["ping", "-c", "1", host])

# ok: command-injection
subprocess.run("uptime", shell=True)

# semgrep-practice

A small Flask app for practicing custom Semgrep rules, SAST pipeline design, and dependency (SCA) scanning.

> **Warning:** `app/vulnerable.py` is insecure on purpose. Do not deploy it, expose it to a network, or copy it into real code.

## Layout

```
pyproject.toml, uv.lock   uv project; requests is pinned to a vulnerable version on purpose
app/vulnerable.py      10 classes of bug
app/fixed.py           the same routes, fixed
rules/<id>.yaml        one custom rule per bug class
rules/<id>.py          rule unit tests (# ruleid: / # ok: annotations)
scripts/check_coverage.py   every rule must fire on vulnerable.py and stay silent on fixed.py
tests/test_fixed.py    proves the fixes block the attacks at runtime
.github/workflows/semgrep.yml   CI pipeline
```

| Rule | Mode | CWE |
|---|---|---|
| `flask-sqli` | taint | 89 |
| `flask-command-injection` | taint | 78 |
| `flask-path-traversal` | taint + sanitizer | 22 |
| `flask-ssrf` | taint + sanitizer | 918 |
| `flask-code-injection` | taint | 95 |
| `insecure-deserialization` | pattern | 502 |
| `weak-hash` | pattern | 328 |
| `hardcoded-secret-key` | pattern | 798 |
| `flask-debug-enabled` | pattern | 489 |
| `requests-verify-disabled` | pattern | 295 |

### The third-party dependency

`requests==2.31.0` is locked in `uv.lock` on purpose. It has known advisories, including CVE-2024-35195 (`verify=False` on a Session sticks to later requests) and CVE-2024-47081 (`.netrc` credential leak). Two kinds of scan look at it:

- **Your code's use of the library (SAST, Semgrep CE):** `flask-ssrf` and `requests-verify-disabled` flag how `app/vulnerable.py` calls `requests`.
- **The library version itself (SCA):** the `dependency-audit` job runs `pip-audit` on the lockfile, free and with no account. With a `SEMGREP_APP_TOKEN` and Supply Chain enabled, `semgrep ci` also reads `uv.lock` and reports whether the vulnerable code paths are *reachable* from your code.

## Run locally

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync                                       # creates .venv from uv.lock

uvx semgrep --test rules/                     # rule unit tests
uvx semgrep scan --config rules/ app/         # 11 findings, all in vulnerable.py
uvx semgrep scan --config rules/ app/ --json --quiet | python3 scripts/check_coverage.py
uv run pytest -q                              # fixed app blocks the attacks

# dependency audit (SCA)
uv export --frozen --no-dev --format requirements-txt -o requirements.lock.txt
uvx pip-audit -r requirements.lock.txt --no-deps --disable-pip

uv run flask --app app.vulnerable run         # http://127.0.0.1:5000/user?name=' OR '1'='1
```

## CI pipeline design

| Job | Runs on | Blocks merge? | Purpose |
|---|---|---|---|
| `rule-tests` | push, PR | yes | Rules are code: validate, unit-test, check coverage |
| `app-tests` | push, PR | yes | `uv lock --check`, then pytest: fixes work at runtime, not just in the scanner |
| `dependency-audit` | push, PR | no | `pip-audit` on `uv.lock`, results in the run summary |
| `pr-gate` | PR | yes | `--baseline-commit`: fails only on **new** findings from the custom rules |
| `full-scan` | push, PR | no | Custom rules + `p/python` as SARIF in the **Security → Code scanning** tab |
| `semgrep-platform` | push, PR | no | `semgrep ci` to Semgrep AppSec Platform (Code + Supply Chain), only if the `SEMGREP_APP_TOKEN` secret is set |

Why it's built this way:

- **Block on high-confidence rules, report the rest.** Registry rules flag two safe lines in `fixed.py`: `path-traversal-open` on a `safe_join` path, and `ssrf-requests` on an allowlist lookup. The custom rules declare both as sanitizers and stay quiet. If you block merges on noisy rules, developers learn to ignore the scanner.
- **Diff-aware gating.** Existing debt (all of `vulnerable.py`) never fails a PR. A PR that adds a new injection does.
- **Test the rules the same way you test the app.** A rule edit that stops matching a known bug fails CI.

To enforce it, protect `main` (**Settings → Branches**) and require `rule-tests`, `app-tests`, and `pr-gate`.

## Exercises

1. Add `subprocess.Popen(cmd, shell=True)` and `os.popen()` cases to `rules/flask-command-injection.py`. Do they pass?
2. `flask-ssrf` trusts any dict named `ALLOWED*` as an allowlist. Write an `# ok:` test that shows the false negative this convention allows, then think of a stricter design.
3. Add a sanitizer to `flask-sqli` for `int(...)` casts and add tests for it.
4. Write a new rule for `jwt.decode(..., options={"verify_signature": False})`, with a vulnerable route, a fixed route, and tests.
5. Add `--config p/owasp-top-ten` to `full-scan` and triage the findings in the Security tab.
6. Open a PR that adds a vulnerable route and watch `pr-gate` fail.
7. Add an `autofix` (`fix:`) to `weak-hash` and a `rules/weak-hash.fixed.py` to test it.
8. Bump `requests` to the latest release in `pyproject.toml`, run `uv lock`, and confirm `dependency-audit` comes back clean. Then compare: which findings did the SAST rules still report?
9. Turn on Semgrep Supply Chain and compare its *reachable* vs *unreachable* findings with pip-audit's flat list.

Rule syntax: https://semgrep.dev/docs/writing-rules/rule-syntax · Playground: https://semgrep.dev/playground

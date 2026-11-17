# semgrep-practice

A beginner playground for writing [Semgrep](https://semgrep.dev) rules.

> **Warning:** `app.py` has security bugs on purpose. Never deploy it.

```
app.py        a tiny Flask app with 4 bugs
rules/        one rule per bug: <id>.yaml is the rule, <id>.py is its test
```

| Rule | What it finds | Rule style |
|---|---|---|
| `hardcoded-secret` | secret key written in code | one `pattern` |
| `requests-no-verify` | HTTPS checks turned off | one `pattern` with a `$METAVARIABLE` |
| `command-injection` | `shell=True` with a built-up command | `patterns` + `pattern-not` |
| `sql-injection` | user input in SQL text | taint mode (follows data) |

## Run it

Needs [uv](https://docs.astral.sh/uv/).

```bash
uvx semgrep --test rules/                 # do the rules work?
uvx semgrep scan --config rules/ app.py   # what do they find in the app?
```

## How rule tests work

In `rules/<id>.py`, put a comment above each line of test code:

- `# ruleid: <id>` means "the rule MUST match the next line".
- `# ok: <id>` means "the rule must NOT match the next line".

`semgrep --test rules/` fails if any of these are wrong.

## See findings in Cursor

1. Install the **Semgrep** extension (Extensions panel, search "Semgrep").
2. Open Settings, search `semgrep.scan.configuration`, and add the **full path** to this repo's `rules/` folder, e.g. `/Users/you/semgrep-practice/rules/`. (A relative path like `rules/` does not work.)
3. In the same settings, turn **off** `Semgrep › Scan: Only Git Dirty`, or you only see findings on lines changed since your last commit.
4. Open `app.py`. The bugs get underlined; hover for the message, or see them all in the **Problems** panel.

After you edit a rule, run **Semgrep: Update rules** from the Command Palette (Cmd+Shift+P).

## CI

`.github/workflows/semgrep.yml` runs on every push and pull request: it tests the rules, then scans `app.py`.

## Try next

1. Add a 5th bug to `app.py` (e.g. `app.run(debug=True)`), then write a rule and a test file for it.
2. In `rules/command-injection.py`, add an `os.system(cmd)` case. Does the rule catch it? Change the rule so it does.
3. Experiment in the [Semgrep Playground](https://semgrep.dev/playground) before saving a rule here.

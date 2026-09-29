# security-reviewer-demo

A small Flask API built to evaluate a **security-focused AI pull-request reviewer**.
The reviewer intentionally ignores ordinary correctness/style issues and reports only
high-confidence security vulnerabilities.

## Demo design

- `main` is the safe baseline.
- `insecure-demo` introduces six planted vulnerabilities.
- Open a PR from `insecure-demo` into `main`.
- Comment `@security-reviewer review` on the PR.
- The Bedrock-powered reviewer analyzes the diff and posts security findings inline.

This is intentionally narrow: the goal is to measure how well a specialized security
agent finds known vulnerabilities, not to build a production application.

## Planted vulnerability answer key

| File | Vulnerability | Expected category |
| --- | --- | --- |
| `app/db.py` | Username lookup builds SQL with string interpolation | SQL injection / CWE-89 |
| `app/users.py` | Authenticated users can request any user ID | Broken access control / IDOR / CWE-639 |
| `app/auth.py` | Source contains a hard-coded service credential | Hard-coded secret / CWE-798 |
| `app/auth.py` | Login logs the supplied plaintext password | Sensitive information in logs / CWE-532 |
| `app/files.py` | User-controlled path is joined without containment validation | Path traversal / CWE-22 |
| `app/preferences.py` | Request-controlled bytes are passed to `pickle.loads` | Unsafe deserialization / CWE-502 |

All credentials/tokens in this repository are fake demo values.

## Run the app/tests locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
python -m app.main
```

The seeded demo users are:

- `alice` / `alice-password`
- `bob` / `bob-password`
- `admin` / `admin-password`

## Run the AI reviewer locally

```bash
pip install -r .github/security-reviewer/requirements.txt
export GITHUB_TOKEN=$(gh auth token)
export AWS_REGION=us-west-2
python .github/security-reviewer/review.py <owner>/<repo> <pr-number> --dry-run
```

The default model is `openai.gpt-oss-120b-1:0`, matching the structure of the
existing Bandwidth reviewer demo. Override it with `MODEL_ID` if needed.

## GitHub Actions setup

Add one of the following credential setups under **Settings → Secrets and variables → Actions**:

- `AWS_BEARER_TOKEN_BEDROCK`, or
- `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY`

Optional variables:

- `AWS_REGION` (defaults to `us-west-2`)
- `MODEL_ID`

Then open the demo PR and comment:

```text
@security-reviewer review
```

## Suggested evaluation

Record:

- planted vulnerabilities: 6
- true positives caught
- vulnerabilities missed
- false positives
- average confidence
- latency
- input/output tokens

This makes it easy to compare a security-specialized prompt/agent against a general-purpose reviewer.

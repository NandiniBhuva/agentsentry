# agentwatch 🔍

> Audit AI agent config files for dangerous permissions and risky tool combinations.

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

AI agents are getting powerful enough to read your email, write to your database, and push code to GitHub. But most agent frameworks hand out permissions with no guardrails.

**agentwatch** is a CLI tool that audits your agent config files and flags:
- 🔴 Overly broad scopes (`full`, `unrestricted`, `admin`, `*`)
- 🟠 Write/destructive permissions (`delete`, `write`, `drop`, `send`)
- 🔴 Dangerous tool combinations (file + network = exfiltration risk)
- 🔴 Sensitive resource access (`secrets`, `credentials`, `api_key`)

And with `--ai`, it goes further — using LLaMA 3.3 (via Groq) to explain each risk in plain English, suggest concrete fixes, and write an executive summary a CISO can actually understand.

Think of it as `npm audit` but for AI agent permissions.

---

## Install

```bash
git clone https://github.com/NandiniBhuva/agentwatch.git
cd agentwatch
python3 -m venv venv && source venv/bin/activate
pip install -e .
```

Or directly via pip:

```bash
pip install git+https://github.com/NandiniBhuva/agentwatch.git
```

---

## Usage

### Basic audit (rule-based, no API key needed)
```bash
agentwatch audit your_agent.yaml
```

### Full AI-powered audit
```bash
export GROQ_API_KEY="your-key-here"
agentwatch audit your_agent.yaml --ai
```

Get a free Groq API key at [console.groq.com](https://console.groq.com) — no credit card required.

---

## Example Output

**Rule-based scan:**
╭──────────────────────────────────────────╮
│ agentwatch — AI Agent Permission Auditor │
╰──────────────────────────────────────────╯
Scanning: sample_agent.yaml
╭──────────────┬────────────────────────┬─────────────────────────────────────────────────╮
│   Severity   │ Tool                   │ Finding                                         │
├──────────────┼────────────────────────┼─────────────────────────────────────────────────┤
│     HIGH     │ gmail_tool             │ Tool has write/destructive permissions: write,   │
│              │                        │ delete                                          │
│   CRITICAL   │ web_browser            │ Tool has overly broad scope — found: unrestricted│
│   CRITICAL   │ file + network         │ File system + network access together = data     │
│              │                        │ exfiltration risk.                              │
│   CRITICAL   │ github + secrets       │ GitHub + secrets access = secret leakage risk.  │
╰──────────────┴────────────────────────┴─────────────────────────────────────────────────╯
╭────────────── Audit Result ──────────────╮
│   Risk Score : 100/100                   │
│   Risk Level : CRITICAL                  │
│   Findings   : 8 total (4 CRITICAL, 4 HIGH) │
╰──────────────────────────────────────────╯

**With `--ai` flag, additionally outputs:**
────────────────── AI Security Analysis ──────────────────
Executive Summary:
The research-assistant AI agent configuration poses significant security risks,
including data exfiltration, phishing, and secret leakage...
Finding Analysis + Fixes:

[HIGH] gmail_tool: The gmail_tool has permissions to write and delete emails,
which could be used to send spam or delete important emails...
Fix: Restrict gmail_tool permissions to only "read" scope...

Overall Recommendation:
Immediately review and restrict the permissions and scopes of all agent tools
to prevent potential security risks and data breaches.

---

## Supported Config Formats

agentwatch parses agent configs from any framework that uses YAML or JSON:

| Framework | Config Format |
|---|---|
| LangChain | `.yaml` / `.json` |
| CrewAI | `.yaml` |
| AutoGen | `.json` |
| Custom agents | `.yaml` / `.json` |

---

## What It Checks

### Permission Risks
| Check | Severity | Example |
|---|---|---|
| Write/destructive access | HIGH | `delete`, `write`, `send` |
| Overly broad scope | CRITICAL | `unrestricted`, `full`, `admin`, `*` |
| Sensitive resource access | CRITICAL | `secrets`, `api_key`, `credentials` |

### Dangerous Combinations
| Combination | Severity | Why It's Risky |
|---|---|---|
| file + network | CRITICAL | Agent can read files and exfiltrate them |
| github + secrets | CRITICAL | Agent can expose stored API keys |
| code + execute | CRITICAL | Agent can write and run arbitrary code |
| database + delete | CRITICAL | Agent can wipe entire databases |
| browser + password | CRITICAL | Agent can steal saved credentials |
| email + contacts | HIGH | Agent can harvest and spam contacts |
| slack + file | HIGH | Agent can leak files via Slack |
| calendar + email | MEDIUM | Agent can send deceptive meeting invites |

---

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | LOW or MEDIUM risk — safe to proceed |
| `1` | HIGH or CRITICAL risk — action required |

Exit code `1` on HIGH/CRITICAL makes agentwatch usable in CI/CD pipelines to block deployments of over-permissioned agents.

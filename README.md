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

**Rule-based scan and with `--ai` flag, additionally outputs:**
<img width="1470" height="956" alt="Screenshot 2026-06-06 at 3 32 02 PM" src="https://github.com/user-attachments/assets/a5bf68d4-142b-410d-92ab-17a98488a33a" />


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

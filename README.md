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

Think of it as `npm audit` but for AI agent permissions.

---

## Install

```bash
git clone https://github.com/NandiniBhuva/agentwatch.git
cd agentwatch
python3 -m venv venv && source venv/bin/activate
pip install -e .
```

## Usage

```bash
agentwatch audit your_agent.yaml
```

## Example Output
<img width="1457" height="349" alt="Screenshot 2026-06-05 at 3 37 02 PM" src="https://github.com/user-attachments/assets/e4878441-c140-4a2c-a741-76ff96cd053d" />

## Supported Config Formats

agentwatch parses agent configs from any framework that uses YAML or JSON:

| Framework | Config Format |
|---|---|
| LangChain | `.yaml` / `.json` |
| CrewAI | `.yaml` |
| AutoGen | `.json` |
| Custom agents | `.yaml` / `.json` |

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

## Exit Codes

| Code | Meaning |
|---|---|
| `0` | LOW or MEDIUM risk — safe to proceed |
| `1` | HIGH or CRITICAL risk — action required |

This makes agentwatch usable in CI/CD pipelines to block deployments of over-permissioned agents.


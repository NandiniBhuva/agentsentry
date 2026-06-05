# Each entry defines a dangerous combination:
# - "combo": two tool-type keywords that together are risky
# - "severity": how bad it is
# - "message": human-readable explanation of why it's risky

DANGEROUS_COMBOS = [
    {
        "combo": ["file", "network"],
        "severity": "CRITICAL",
        "message": "File system + network access together = data exfiltration risk. "
                   "Agent could read local files and send them externally."
    },
    {
        "combo": ["email", "contacts"],
        "severity": "HIGH",
        "message": "Email + contacts access = phishing/spam risk. "
                   "Agent could harvest contacts and send unsolicited messages."
    },
    {
        "combo": ["code", "execute"],
        "severity": "CRITICAL",
        "message": "Code generation + execution access = arbitrary code execution risk. "
                   "Agent could write and run malicious code."
    },
    {
        "combo": ["database", "delete"],
        "severity": "CRITICAL",
        "message": "Database + delete access = irreversible data loss risk. "
                   "Agent could wipe entire tables or databases."
    },
    {
        "combo": ["calendar", "email"],
        "severity": "MEDIUM",
        "message": "Calendar + email access = social engineering risk. "
                   "Agent could read your schedule and send deceptive meeting invites."
    },
    {
        "combo": ["browser", "password"],
        "severity": "CRITICAL",
        "message": "Browser + password/credential access = credential theft risk. "
                   "Agent could access saved passwords in the browser."
    },
    {
        "combo": ["github", "secrets"],
        "severity": "CRITICAL",
        "message": "GitHub + secrets access = secret leakage risk. "
                   "Agent could expose API keys or tokens stored in repositories."
    },
    {
        "combo": ["slack", "file"],
        "severity": "HIGH",
        "message": "Slack + file access = data leakage risk. "
                   "Agent could exfiltrate files by posting them to Slack channels."
    },
]


def _get_tool_fingerprint(tools: list) -> list:
    """
    Flatten all tool names and their config values into a single
    list of lowercase strings — this is what we match combos against.
    """
    fingerprint = []

    for tool in tools:
        if isinstance(tool, str):
            fingerprint.append(tool.lower())
        elif isinstance(tool, dict):
            # Add the tool name
            name = tool.get("name") or tool.get("type") or ""
            fingerprint.append(name.lower())

            # Also add any string values inside the tool config
            for v in tool.values():
                if isinstance(v, str):
                    fingerprint.append(v.lower())
                elif isinstance(v, list):
                    for item in v:
                        if isinstance(item, str):
                            fingerprint.append(item.lower())

    return fingerprint


def analyze_combinations(config: dict) -> list:
    """
    Scan the full set of agent tools for dangerous combinations.
    Returns a list of findings.
    """
    findings = []

    tools = (
        config.get("tools")
        or config.get("capabilities")
        or config.get("actions")
        or []
    )

    if not tools:
        return findings

    # Get a flat fingerprint of everything in the tool list
    fingerprint = _get_tool_fingerprint(tools)

    for combo_rule in DANGEROUS_COMBOS:
        keyword_a, keyword_b = combo_rule["combo"]

        # Check if BOTH keywords appear anywhere in the agent's tool fingerprint
        a_found = any(keyword_a in value for value in fingerprint)
        b_found = any(keyword_b in value for value in fingerprint)

        if a_found and b_found:
            findings.append({
                "severity": combo_rule["severity"],
                "tool": f"{keyword_a} + {keyword_b}",
                "message": combo_rule["message"]
            })

    return findings
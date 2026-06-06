# Keywords that suggest write or destructive access
WRITE_KEYWORDS = [
    "write", "delete", "remove", "drop", "destroy",
    "modify", "update", "edit", "insert", "create",
    "truncate", "overwrite", "send", "post", "put", "patch"
]

# Keywords that suggest dangerously broad access
BROAD_SCOPE_KEYWORDS = [
    "all", "full", "unrestricted", "unlimited", "wildcard",
    "admin", "root", "superuser", "global", "*"
]

# Keywords that suggest highly sensitive resource access
SENSITIVE_RESOURCE_KEYWORDS = [
    "password", "secret", "credential", "token", "key",
    "ssn", "pii", "billing", "payment", "credit_card",
    "private_key", "api_key"
]


def _flatten_values(obj, depth=0) -> list:
    """
    Recursively extract all string values from a nested dict/list.
    We use this to scan every field in a tool's config, not just the top level.
    Limit depth to 5 to avoid infinite recursion on weird configs.
    """
    if depth > 5:
        return []

    results = []

    if isinstance(obj, str):
        results.append(obj.lower())
    elif isinstance(obj, list):
        for item in obj:
            results.extend(_flatten_values(item, depth + 1))
    elif isinstance(obj, dict):
        for v in obj.values():
            results.extend(_flatten_values(v, depth + 1))

    return results


def analyze_permissions(config: dict) -> list:
    """
    Scan agent config for risky permissions.
    Returns a list of findings, each with severity, tool, and message.
    """
    findings = []

    # Get the list of tools — handle common config formats
    # Some frameworks use "tools", some use "capabilities", some use "actions"
    tools = (
        config.get("tools")
        or config.get("capabilities")
        or config.get("actions")
        or []
    )

    if not tools:
        return findings  # No tools defined, nothing to analyze

    for tool in tools:
        # Tools can be a string (just a name) or a dict (name + config)
        if isinstance(tool, str):
            tool_name = tool
            tool_values = [tool.lower()]
        elif isinstance(tool, dict):
            tool_name = tool.get("name") or tool.get("type") or "unnamed_tool"
            tool_values = _flatten_values(tool)
        else:
            continue

        # --- Check 1: Write / destructive access ---
        matched_write = [kw for kw in WRITE_KEYWORDS if kw in tool_values]
        if matched_write:
            findings.append({
                "severity": "HIGH",
                "tool": tool_name,
                "message": f"Tool has write/destructive permissions: {', '.join(matched_write)}"
            })

        # --- Check 2: Overly broad scopes ---
        matched_broad = [kw for kw in BROAD_SCOPE_KEYWORDS if kw in tool_values]
        if matched_broad:
            findings.append({
                "severity": "CRITICAL",
                "tool": tool_name,
                "message": f"Tool has overly broad scope — found: {', '.join(matched_broad)}"
            })

        # --- Check 3: Sensitive resource access ---
        matched_sensitive = [kw for kw in SENSITIVE_RESOURCE_KEYWORDS if kw in tool_values]
        if matched_sensitive:
            findings.append({
                "severity": "CRITICAL",
                "tool": tool_name,
                "message": f"Tool accesses sensitive resources: {', '.join(matched_sensitive)}"
            })

    return findings
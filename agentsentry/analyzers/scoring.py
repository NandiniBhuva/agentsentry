# How much each severity level contributes to the total risk score
SEVERITY_WEIGHTS = {
    "CRITICAL": 40,
    "HIGH":     20,
    "MEDIUM":   10,
    "LOW":       5,
}

# Score thresholds that map to a final risk level
RISK_LEVELS = [
    (80, "CRITICAL"),
    (50, "HIGH"),
    (20, "MEDIUM"),
    (0,  "LOW"),
]

# Color codes for display (used later in report.py)
RISK_COLORS = {
    "CRITICAL": "bold red",
    "HIGH":     "bold orange1",
    "MEDIUM":   "bold yellow",
    "LOW":      "bold green",
}


def calculate_score(findings: list) -> dict:
    """
    Takes a combined list of findings and returns a score summary:
    - raw_score: numeric score (can exceed 100, we cap it)
    - score: capped at 100
    - level: LOW / MEDIUM / HIGH / CRITICAL
    - color: for rich terminal display
    - counts: how many findings per severity
    - total: total number of findings
    """

    # Count findings by severity
    counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for finding in findings:
        severity = finding.get("severity", "LOW")
        if severity in counts:
            counts[severity] += 1

    # Calculate raw score by multiplying count × weight for each severity
    raw_score = sum(counts[sev] * SEVERITY_WEIGHTS[sev] for sev in counts)

    # Cap the score at 100
    score = min(raw_score, 100)

    # Determine risk level based on score thresholds
    level = "LOW"
    for threshold, label in RISK_LEVELS:
        if score >= threshold:
            level = label
            break

    return {
        "raw_score": raw_score,
        "score": score,
        "level": level,
        "color": RISK_COLORS[level],
        "counts": counts,
        "total": len(findings),
    }
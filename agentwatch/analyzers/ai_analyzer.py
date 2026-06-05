import os
import yaml
from google import genai

# Configure the Gemini client using the API key from environment
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))


def analyze_with_ai(config: dict, findings: list) -> dict:
    """
    Takes the agent config and rule-based findings, sends them to Gemini,
    and returns an AI-powered analysis with explanations, fixes, and a summary.

    Returns a dict with:
    - success: whether the AI call succeeded
    - summary: executive summary of the overall risk
    - finding_analysis: detailed explanation of each finding
    - missed_risks: anything the rules missed
    - recommendation: one-line action item
    """

    if not findings:
        findings_text = "No issues were flagged by the automated rules."
    else:
        findings_text = "\n".join([
            f"- [{f['severity']}] {f['tool']}: {f['message']}"
            for f in findings
        ])

    config_text = yaml.dump(config, default_flow_style=False)

    prompt = f"""
You are a senior AI security analyst specializing in AI agent permission auditing.

You are reviewing an AI agent configuration file. An automated rule-based scanner
has already flagged some issues. Your job is to:

1. Provide a plain English explanation of WHY each finding is dangerous
2. Give a concrete, specific fix for each finding
3. Write a 2-3 sentence executive summary a non-technical CISO can understand
4. Flag anything the automated scanner may have MISSED

--- AGENT CONFIG ---
{config_text}

--- AUTOMATED FINDINGS ---
{findings_text}

Respond in this exact format:

EXECUTIVE SUMMARY:
[2-3 sentences explaining the overall risk level and what's at stake]

FINDING ANALYSIS:
[For each finding, explain why it's dangerous and give a specific fix]

MISSED RISKS:
[Any additional risks you spotted that the automated scanner didn't catch. If none, write "None identified."]

OVERALL RECOMMENDATION:
[One sentence on what the team should do first]
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-lite",
            contents=prompt
        )
        response_text = response.text

        sections = _parse_response(response_text)
        return {
            "success": True,
            "summary": sections.get("EXECUTIVE SUMMARY", "").strip(),
            "finding_analysis": sections.get("FINDING ANALYSIS", "").strip(),
            "missed_risks": sections.get("MISSED RISKS", "").strip(),
            "recommendation": sections.get("OVERALL RECOMMENDATION", "").strip(),
            "raw_response": response_text
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "summary": "",
            "finding_analysis": "",
            "missed_risks": "",
            "recommendation": ""
        }


def _parse_response(text: str) -> dict:
    """
    Splits the AI response into labeled sections.
    Each section starts with a label like 'EXECUTIVE SUMMARY:'
    """
    sections = {}
    current_section = None
    current_lines = []

    for line in text.splitlines():
        stripped = line.strip()
        if stripped.endswith(":") and stripped.upper() == stripped:
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = stripped[:-1]
            current_lines = []
        else:
            if current_section:
                current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections
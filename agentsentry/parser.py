import yaml
import json
import os

def load_agent_config(filepath: str) -> dict:
    """
    Load an agent config file (YAML or JSON) and return it as a dictionary.
    Supports .yaml, .yml, and .json formats.
    """

    # Check if the file actually exists before trying to open it
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Config file not found: {filepath}")

    # Grab the file extension so we know how to parse it
    _, ext = os.path.splitext(filepath.lower())

    if ext not in [".yaml", ".yml", ".json"]:
        raise ValueError(f"Unsupported file format '{ext}'. Use .yaml, .yml, or .json")

    with open(filepath, "r") as f:
        if ext in [".yaml", ".yml"]:
            config = yaml.safe_load(f)
        elif ext == ".json":
            config = json.load(f)

    # Handle completely empty files
    if config is None:
        raise ValueError(f"Config file is empty: {filepath}")

    # We expect the config to be a dictionary at the top level
    if not isinstance(config, dict):
        raise ValueError(f"Config file must be a YAML/JSON object at the top level, got: {type(config).__name__}")

    return config
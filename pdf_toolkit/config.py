import json
from pathlib import Path

_DEFAULTS = {
    "input_dir": "input",
    "output_dir": "output",
}

def load_config():
    """
    Load config.json from the project root.
    Falls back to defaults if config.json is missing
    or missing specific keys.
    Returns a dict like:
        {
            "input_dir": "input",
            "output_dir": "output"
        }
    """
    # config.json lives one level above this package directory
    project_root = Path(__file__).resolve().parent.parent
    config_path = project_root / "config.json"

    config_data = {}
    if config_path.exists():
        try:
            with open(config_path, "r") as f:
                config_data = json.load(f)
        except json.JSONDecodeError:
            # if config.json is corrupted, we just ignore and fall back to defaults
            config_data = {}

    # merge defaults with whatever we loaded
    merged = {**_DEFAULTS, **config_data}
    return merged